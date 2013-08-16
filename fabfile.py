from fabric.api import *

env.hosts = ["sonofshelf"]
env.sudo_user = "jobs"

@with_settings(sudo_user="root")
def restart(unit):
    """Enable and restart a systemd unit."""
    sudo("systemctl reenable {}".format(unit))
    sudo("systemctl restart {}".format(unit))

@with_settings(sudo_user="root")
def systemd_unit(name):
    """Install, enable and restart a systemd unit."""
    put("systemd_units/{}.service".format(name),
        "/etc/systemd/system/",
        use_sudo=True)
    restart(name)

def checkout(remote, dir):
    """Check out a git repo into a directory.
    Beware: This will throw away all changes!
    """
    sudo("mkdir -p %s" % dir)
    with cd(dir):
        sudo("git init -q")
        sudo("git fetch {}".format(remote))
        sudo("git reset --hard FETCH_HEAD")
        sudo("git clean -df")

@task
@with_settings(sudo_user="root")
def dnsmasq():
    put("configs/dnsmasq.conf", "/etc/dnsmasq.conf", use_sudo=True)
    restart("dnsmasq")

@task
@with_settings(sudo_user="root")
def sshd():
    put("configs/ssh/sshd_config", "/etc/ssh/sshd_config", use_sudo=True)
    restart("sshd")

@task
def shetserv():
    checkout("https://github.com/18sg/SHET.git", "/home/jobs/SHET")
    with cd("/home/jobs/SHET"):
        sudo("python2 setup.py install --user")
    systemd_unit("shetserv")

@task
def shetsource():
    checkout("https://github.com/18sg/SHETSource.git", "/home/jobs/SHETSource")
    systemd_unit("shetrouter")

@task
def shetsource_tcp():
    checkout("https://github.com/18sg/SHETSource.git", "/home/jobs/SHETSourceTCP")
    systemd_unit("shetroutertcp")

@task
def underground():
    randomshetclients()
    systemd_unit("shetunderground")

@task
def shetlights():
    underground()
    checkout("https://github.com/18sg/SHETLights.git", "/home/jobs/SHETLights")
    systemd_unit("shetlights")

@task
def shetlights_tom():
    checkout("https://github.com/18sg/SHETLights.git", "/home/jobs/SHETLightsTom")
    systemd_unit("shetlights_tom")

@task
def randomshetclients():
    checkout("https://github.com/18sg/Random-SHET-Clients.git",
             "/home/jobs/Random-SHET-Clients")

@task
def onkyo():
    systemd_unit("shetonkyo")
