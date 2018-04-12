# smap-driver-xovis

A driver for [Xovis](https://www.xovis.com) camera counters.

## Dependencies

- `python3.5` for Python with AsyncIO.
- `python3-aiohttp` for HTTP operations.

## Features

- Buffering: none (each camera buffers)
- Discovery: manual (each camera is configured to push to the driver)

## Configuration

The storage engine specifc configuration options are given at the commandline after `run` and the name of the storage engine.

The remaining options are given in the `/etc/config.json` configuration file. These are also available to the storage engines. It contains the following keys:

- `interface` The interface to listen on.
- `port` The port to listen on.
- `sourcename` The sMAP sourcename (**Note:** This is specific to the smap storage engine)
- `uuid` The instance base uuid (**Note:** This is specific to the smap storage engine)
- `uptime_delay` The time in seconds between uptime posts.
- `log/blacklist` A list of event identifiers *not* to log.

### Cameras

Go the the *Config* tab of the webpage exposed by the camera. Under the *Settings* section open the *Data Push* tab, enter the following configuration and click *Add*:

- **Data Type** Line count data
- **Interval** 1 minute
- **Granularity** 1 minute
- **Protocol** HTTP(S)
- **Data push format** JSON
- **URL** The URL of the service being exposed by the driver

The go to the top of the page and click *Save*.

## Starting

The full description of command line options::
```shell
./xovis-driver help
```

Example:
```shell
./xovis-driver run smap http://server.dk:8079/add/cac7d1e0-17d8-4c87-b0e3-aa6b27e7f7f6 &> ../log/driver.log
```

## Debugging

The logs printed to STDOUT should contain everything needed for debugging.

## Writing a Storage Engine

Any `.py` file under `/src/storage_engines/` is immediately availabile under the name of the file. Start out by copying `/src/storage_engines/demo.py` to `/src/storage_engines/myengine.py`.

Then try [configuring a camera](#cameras) and then start the engine by running:

```shell
./xovis-driver run myengine one two
```

This will print out the all data delivered to the storage engine, annotated for navigation. It is up to the storage engine writer to decide what to do with this information. The storage engine should refrain from performing any logic at load-time.

The main argument to the `insert` function is a data structure of the form: `element-name ↦ direction ↦ {'readings' ↦ (timestamp × value) list, 'meta' ↦ name ↦ value}`.

