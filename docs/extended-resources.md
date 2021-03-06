# Extended Resources

## Simulating windows

I can grep tails of the tcp log for various reasons.

- To grep the whole log then continue grepping the tail: `tail -f -n +1 log.log | grep "stuff"`
    - Can write regexes now for these text streams, to some degree.

## Socket and Stream Handling

The socket by default uses `\r\n` carriage returns, which look like `^M` and a newline in vim.

It might be a good idea to find a library for handling tcp instead of doing it myself.

This isn't my core problem though, so maybe do this later.  What I have works.

- [Exscript: for ssh and telnet connections](https://exscript.readthedocs.io/en/latest/index.html)
- [Pexpect: control a subprocess like telnet... not really for this](https://github.com/pexpect/pexpect)


## Other Dragonrealms Client Implementations

Here is some info about implementing a client: https://www.reddit.com/r/dragonrealms/comments/4e0e3h/host_name_and_port_number/

EAccess Protocol (get a token from user/pass): http://warlockclient.wikia.com/wiki/EAccess_Protocol

More eaccess (aka SGE Protocol): https://gswiki.play.net/SGE_protocol/saved_posts

stormfront protocol (warlock): http://warlockclient.wikia.com/wiki/StormFront_Protocol

A client that can interact and authenticate with an API service is sufficient. This can easily be done with react.
    - Client should be on a website
    - Client should poll state and refresh the UI
    - Client should be easy to type into
    - Client should have options to offer rich features

### Here is an elanthipedia entry on front ends

- https://elanthipedia.play.net/Front_end


## Simple POC

To connect to dragonrealms, 

- get a wizard version SAL file
    - You may need to spoof a windows internet explorer user agent in your browser
- get your game key from a `Charactername.sal` file.
- get the host and port from the `sal` file.
- `telnet host port`
    - or use `rlwrap telnet host port` for a readline wrapper (so you can enter commands without scroll)
- send the first line with only your `game key`
- press enter and then add a `\r` for newline (`\n` works in python, maybe just two newlines)
    - whitespace will probably work too?
- after the first newline, send the client string and a second newline
- after the fourth line, which is the second newline, the game will connect

