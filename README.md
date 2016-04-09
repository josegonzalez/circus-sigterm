# circus-sigterm

A small reproduction for invalid signal passing by circus `0.13`.

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
2. Install `circus==0.13` globally
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

### strace

You can also `strace` the process being watched to see what signals it is getting:

```shell
strace -p $(ps auxf | grep [p]ython | grep -v bin | awk '{print $2}')
```

This results in the following type of output for a direct `kill` signal:

```
Process 7013 attached
write(1, "sleeping", 8)                 = 8
write(1, "\n", 1)                       = 1
select(0, NULL, NULL, NULL, {1, 0})     = ? ERESTARTNOHAND (To be restarted if no handler)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6701, si_uid=900} ---
rt_sigreturn()                          = -1 EINTR (Interrupted system call)
write(1, "Received 13", 11)             = 11
write(1, "\n", 1)                       = 1
rt_sigaction(SIGINT, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGHUP, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGQUIT, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGILL, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGTRAP, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGABRT, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGBUS, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGFPE, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGUSR1, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGSEGV, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGUSR2, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGPIPE, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGALRM, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGTERM, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGCHLD, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGCONT, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGTSTP, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGTTIN, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGTTOU, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGURG, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGXCPU, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGXFSZ, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGVTALRM, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGPROF, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGWINCH, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGIO, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGPWR, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGSYS, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGRT_2, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
rt_sigaction(SIGRT_32, {SIG_DFL, [], SA_RESTORER, 0x7ff7e0116340}, {0x45a0f5, [], SA_RESTORER, 0x7ff7e0116340}, 8) = 0
exit_group(0)                           = ?
+++ exited with 0 +++
root@vagrant:~#
```

Issuing a `circusctl restart` results in a very different set of logs:

```
Process 6979 attached
write(1, "sleeping", 8)                 = 8
write(1, "\n", 1)                       = 1
select(0, NULL, NULL, NULL, {1, 0})     = 0 (Timeout)
write(1, "sleeping", 8)                 = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
rt_sigreturn()                          = -1 EPIPE (Broken pipe)
write(2, "Traceback (most recent call last"..., 35) = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
rt_sigreturn()                          = -1 EPIPE (Broken pipe)
write(2, "  File \"/vagrant/test.py\", line "..., 48) = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
rt_sigreturn()                          = -1 EPIPE (Broken pipe)
open("/vagrant/test.py", O_RDONLY)      = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=736, ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0566396000
read(3, "#!/usr/bin/env python\n\nimport ti"..., 4096) = 736
write(2, "    ", 4)                     = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
rt_sigreturn()                          = -1 EPIPE (Broken pipe)
write(2, "main()\n", 7)                 = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
rt_sigreturn()                          = -1 EPIPE (Broken pipe)
close(3)                                = 0
munmap(0x7f0566396000, 4096)            = 0
write(1, "Received 13", 11)             = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
rt_sigreturn()                          = -1 EPIPE (Broken pipe)
write(2, "\n", 1)                       = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
rt_sigreturn()                          = -1 EPIPE (Broken pipe)
rt_sigaction(SIGINT, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGHUP, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGQUIT, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGILL, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGTRAP, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGABRT, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGBUS, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGFPE, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGUSR1, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGSEGV, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGUSR2, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGPIPE, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGALRM, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGTERM, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGCHLD, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGCONT, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGTSTP, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGTTIN, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGTTOU, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGURG, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGXCPU, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGXFSZ, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGVTALRM, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGPROF, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGWINCH, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGIO, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGPWR, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGSYS, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGRT_2, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
rt_sigaction(SIGRT_32, {SIG_DFL, [], SA_RESTORER, 0x7f0565f69340}, {0x45a0f5, [], SA_RESTORER, 0x7f0565f69340}, 8) = 0
write(2, "close failed in file object dest"..., 40) = -1 EPIPE (Broken pipe)
--- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=6979, si_uid=900} ---
+++ killed by SIGPIPE +++
```

You can also strace the watcher itself:

```shell
strace -p $(ps auxf | grep [p]ython | grep bin | grep test.py | awk '{print $2}')
```

`kill` to the child results in the following:

```
Process 7077 attached
wait4(-1, [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0, NULL) = 7078
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=7078, si_status=0, si_utime=0, si_stime=0} ---
rt_sigreturn()                          = 7078
exit_group(0)                           = ?
+++ exited with 0 +++
```

And  `circusctl restart` gives us the following:

```
Process 7027 attached
wait4(-1, 0x7ffce3c854cc, 0, NULL)      = ? ERESTARTSYS (To be restarted if SA_RESTART is set)
--- SIGTERM {si_signo=SIGTERM, si_code=SI_USER, si_pid=6677, si_uid=0} ---
+++ killed by SIGTERM +++
```

## under the hood

The `test.py` python script is a simple signal handler that catches all valid signals for a given operating system. This should allow it to catch other signals that circus might be accidentally sending (though notably not `SIGKILL`, `SIGSTOP`, OR `SIG_DFL`).

The environment variable `PYTHONUNBUFFERED` is set to `1` so that python [outputs log messages as they happen](https://docs.python.org/2/using/cmdline.html#cmdoption-u).

Note that we could *also* add `singleton = 1` to the circus watcher configuration, though we would see the same result.
