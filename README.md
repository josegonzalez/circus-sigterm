# circus-sigterm

A small reproduction for invalid signal passing by circus `0.12.1`.

## requirements

- Vagrant (test on 1.7.4 on a OS X 10.10.5 host machine)
- A semi-fast internet connection to download the `bento/ubuntu-14.04` image

## usage

Run the following command:

```shell
vagrant up
```

This will:

1. Install all python requirements
2. Install `circus==0.12.1` globally
3. Start a watcher for `test.ini`

Logs are written to the `/vagrant` directory in the vm, and thus should persist onto the host operating system.

Next, run the following command to connect to the vm:

```shell
vagrant ssh
```

Now issue a `circusctl stop`. This will stop the worker with the following output:

```
Skipping SIGKILL due to (22, 'Invalid argument')
Skipping SIGSTOP due to (22, 'Invalid argument')
Skipping SIG_DFL due to signal number out of range
sleeping
sleeping
sleeping
sleeping
sleeping
sleeping
sleeping
```

Note that there is no final message, simply a lack of progress (the process is also stopped). If you instead kill the child process like so:

```shell
# inside the vm
kill -15 $(ps auxf | grep [p]ython | grep -v bin | awk '{print $2}')
```

This will have the following type of output:

```
Skipping SIGKILL due to (22, 'Invalid argument')
Skipping SIGSTOP due to (22, 'Invalid argument')
Skipping SIG_DFL due to signal number out of range
sleeping
sleeping
sleeping
sleeping
sleeping
sleeping
sleeping
Received 15
```

The process will respawn as the watcher itself is still running and will restart the process since it cannot detect it anymore.

## under the hood

The `test.py` python script is a simple signal handler that catches all valid signals for a given operating system. This should allow it to catch other signals that circus might be accidentally sending (though notably not `SIGKILL`, `SIGSTOP`, OR `SIG_DFL`).

The environment variable `PYTHONUNBUFFERED` is set to `1` so that python [outputs log messages as they happen](https://docs.python.org/2/using/cmdline.html#cmdoption-u).

Note that we could *also* add `singleton = 1` to the circus watcher configuration, though we would see the same result.
