## About

The `perf` script executes commands described in *runner* specifications which
are found in the `runners/` subdirectory to benchmark certain aspects. At the
moment, there are two types of benchmarks: performance benchmarks measuring the
run-time and quality benchmarks which measure image metrics of the output with a
given input. For further analysis, the runner name, parameters and the run time
are saved in a CSV file.  The `perf` script works like the Git binary and
features three commands: `list`, `run` and `chart`. To list all known runners
call

    $ ./perf list

and to run all runners call

    $ ./perf run

To disable one or more runners use

    $ ./perf run --disable foo,bar

and to see more output pass the `--verbose` flag to the `perf` script. To
restrict to certain benchmark types, use

    $ ./perf run --type perf

You can analyze the resulting CSV files with the builtin `chart` command

    $ ./perf chart result-*

which will generate some graphs and an HTML file displaying them and the raw
data. Here is a [demonstration](http://www.ipe.fzk.de/~vogelgesang/tomoperf/) of
such an output.


### Runner specification

A runner specification is a simple top-level JSON object file. The required
fields are `name` and the parameterized `command` list to call. Furthermore
parameters that are known to the runner and not to be supplied by the user are
stored in a `params` dictionary with the parameter name mapping to a list of
values. To prepare the environment, a `prepare` command list can be used and
is populate with the same arguments as the `command` list.

The following is a valid specification:

```json
{
    "name": "foo",
    "params": {
        "age": [12, 13, 14, 28],
        "city": ["New York", "Berlin"]
    },
    "prepare": [
        "bash somescript.sh ${name}"
    ],
    "command": [
        "python",
        "somescript.py",
        "--name", "${name}",
        "--age", "${age}",
        "--city", "${city}"
    ]
}
```

Note the templates denoted by `${xxx}` in the `args` list. If a template cannot
be substituted from a value in the `params` dictionary, it *must be* supplied on
the command line. Therefore, to run this specification you have to call

    $ ./perf run foo --params "name=bar"

Note a final parameter product is computed and passed to the command. That means
the foo specification is run eight times (first with `age=12, city="New York",
name="bar"`, second with `age=12, city="Berlin", name="bar"` and so on).
Similarly to the `args` list you can pass a list of parameters to scan as well,
i.e.

    $ ./perf run foo --params "x=1,2,4 y=5,6"

computes all combinations of `x` and `y`.


## Dependencies

Besides the Python standard library, the `perf` script requires

* daiquiri for logging setup
* marshmallow for loading and validation of runner descriptions

Additionally, the `chart` subcommand requires

* jinja2
* pandas
