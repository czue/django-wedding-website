"""
Server layout:
    ~/services/supervisor/
        holds the configurations for these applications
        for each environment (staging, demo, etc) running on the server.
        Theses folders are included in the /etc/supervisor configuration.
    ~/www/
        This folder contains the code, python environment, and logs
        for each environment (staging, demo, etc) running on the server.
        Each environment has its own subfolder named for its evironment
        (i.e. ~/www/staging/logs and ~/www/demo/logs).
"""
from fabric.context_managers import cd
from fabric.operations import require
from fabric.api import run, execute, task, sudo, env
import os
import posixpath


if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
    env.use_ssh_config = True


env.project = 'bigday'
env.code_branch = 'master'
env.sudo_user = 'czue'

ENVIRONMENTS = ('production',)

@task
def _setup_path():
    env.root = posixpath.join(env.home, 'www', env.environment)
    env.hosts = ['czue.org']
    env.log_dir = posixpath.join(env.home, 'www', env.environment, 'log')
    env.code_root = posixpath.join(env.root, 'code_root')
    env.project_media = posixpath.join(env.code_root, 'media')
    env.virtualenv_root = posixpath.join(env.root, 'python_env')
    env.services = posixpath.join(env.home, 'services')
    env.db = '%s_%s' % (env.project, env.environment)

@task
def production():
    env.home = "/home/czue"
    env.environment = 'bigday'
    env.django_port = '9091'
    _setup_path()


def update_code():
    with cd(env.code_root):
        sudo('git fetch', user=env.sudo_user)
        sudo('git checkout %(code_branch)s' % env, user=env.sudo_user)
        sudo('git reset --hard origin/%(code_branch)s' % env, user=env.sudo_user)
        # remove all .pyc files in the project
        sudo("find . -name '*.pyc' -delete", user=env.sudo_user)

@task
def deploy():
    """
    Deploy code to remote host by checking out the latest via git.
    """

    require('root', provided_by=ENVIRONMENTS)
    try:
        execute(update_code)
        execute(update_virtualenv)
        execute(migrate)
        execute(_do_collectstatic)
    finally:
        # hopefully bring the server back to life if anything goes wrong
        execute(services_restart)
        pass


@task
def update_virtualenv():
    """
    Update external dependencies on remote host assumes you've done a code update.
    """
    require('code_root', provided_by=ENVIRONMENTS)
    files = (
        posixpath.join(env.code_root, 'requirements.txt'),
        posixpath.join(env.code_root, 'deploy', 'prod-requirements.txt'),
    )
    for req_file in files:
        cmd = 'source %s/bin/activate && pip install -r %s' % (
            env.virtualenv_root,
            req_file
        )
        sudo(cmd, user=env.sudo_user)


def touch_supervisor():
    """
    touch supervisor conf files to trigger reload. Also calls supervisorctl
    update to load latest supervisor.conf
    """
    require('code_root', provided_by=ENVIRONMENTS)
    supervisor_path = posixpath.join(posixpath.join(env.services, 'supervisor'), 'supervisor.conf')
    sudo('touch %s' % supervisor_path, user=env.sudo_user)
    _supervisor_command('update')


def services_start():
    ''' Start the gunicorn servers '''
    require('environment', provided_by=ENVIRONMENTS)
    _supervisor_command('update')
    _supervisor_command('reload')
    _supervisor_command('start  all')

def services_stop():
    ''' Stop the gunicorn servers '''
    require('environment', provided_by=ENVIRONMENTS)
    _supervisor_command('stop all')


def services_restart():
    ''' Stop and restart all supervisord services'''
    require('environment', provided_by=ENVIRONMENTS)
    _supervisor_command('stop all')
    _supervisor_command('start  all')


def migrate():
    """ run south migration on remote environment """
    require('code_root', provided_by=ENVIRONMENTS)
    with cd(env.code_root):
        sudo('%(virtualenv_root)s/bin/python manage.py migrate --noinput' % env, user=env.sudo_user)

def _do_collectstatic():
    """
    Collect static after a code update
    """
    with cd(env.code_root):
        sudo('%(virtualenv_root)s/bin/python manage.py collectstatic --noinput' % env, user=env.sudo_user)

@task
def collectstatic():
    """ run collectstatic on remote environment """
    require('code_root', provided_by=ENVIRONMENTS)
    update_code()
    _do_collectstatic()


def _supervisor_command(command):
    require('hosts', provided_by=ENVIRONMENTS)
    sudo('supervisorctl %s' % (command), shell=False, user='root')

@task
def print_supervisor_files():
    for fname in os.listdir('deploy/supervisor'):
        with open(os.path.join('deploy', 'supervisor', fname)) as f:
            print '%s:\n\n' % fname
            print f.read() % env
