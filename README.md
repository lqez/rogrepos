# rogrepos

Well, you've contributed a lot of projects in this world, congrat!
But you must have bunch of outdated repositories in your GitHub account.

Rogrepos helps you remove them, ya. Only you have to do is just choosing yes or no.

```
$ rogrepos
Retrieving organizations from GitHub...

    KeyCastr, 1 public repo(s), 0 private repo(s)
    Summernote, 12 public repo(s), 0 private repo(s)

Retrieving 122 repositories from GitHub...

5 of 122
lqez/Alien-Archive-Npk
    Description: Alien::Archive::Npk Perl 5 module. Alien for neat package system - npk
    Forked     : from am0c/Alien-Archive-Npk
    Updated    : 2014-09-09 14:50:20 / 1191 day(s) ago
    Size       : 60 KB
    Do you really want to delete? [y/N]: n

97 of 122
lqez/yuna
    Description: yuna
    Updated    : 2013-11-27 16:13:40 / 1477 day(s) ago
    Size       : 100 KB
    Do you really want to delete? [y/N]: y
    This is not a forked project. Are you sure? [y/N]: y
lqez/yuna was deleted.
```

Like that.


## Usage

1. Get a token from [GitHub developer settings page](https://github.com/settings/tokens). Note that you have to allow **`repo`** and **`delete_repo`**.

2. Install `rogrepos` by `pip install rogrepos`

3. Run it.

```
$ rogrepos --token=<GITHUB_ACCESS_TOKEN>
```

or 

```
$ token=<GITHUB_ACCESS_TOKEN> rogrepos
```

or put your token in `~/.rogreposrc` and use it.

```
$ echo 'token=<GITHUB_ACCESS_TOKEN>' > ~/.rogreposrc
$ rogrepos
```


## Options

Rogrepos finds outdated repositories from GitHub, over 365 days by default. If you want to filter older projects, use `days` option.

```
$ rogrepos --days=1024
```

You can see other options.

```
$ rogrepos --help
```


## DISCLAIMER

Rogrepos has no responsible for any problems caused by incorrect operation.


## License

MIT
