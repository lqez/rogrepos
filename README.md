# rogrepos
Rogrepos removes outdated GitHub repositories


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

Rogrepos find outdated repositories from GitHub, over 365 days by default. If you want to filter older projects, use `days` option.

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
