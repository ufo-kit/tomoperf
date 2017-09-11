## About

The `run` script executes commands described in *runner* specifications which
are found in the `runners/` subdirectory and measures the run time. For further
analysis, the runner name, parameters and the run time are saved in a CSV file.
The `run` script works like the Git binary and features two commands `run` and
`list` at the moment. To list all known runners call

    $ ./run list

and to run all runners call

    $ ./run run

To run a specific runner use

    $ ./run run --name foo

and to see more output pass the `--verbose` flag to the `run` script.


### Runner specification

A runner specification is a simple top-level JSON object file. The required
fields are `name`, the `command` to call and the parameterized `args` list which
might be empty to call the command with. Furthermore parameters that are known
to the runner and not to be supplied by the user are stored in a `params`
dictionary with the parameter name mapping to a list of values. The following is
a valid specification:

```json
{
    "name": "foo",
    "command": "python",
    "params": {
        "age": [12, 13, 14, 28],
        "city": ["New York", "Berlin"]
    },
    "args": [
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

    $ ./run run foo --params "name=bar"

Note a final parameter product is computed and passed to the command. That means
the foo specification is run eight times (first with `age=12, city="New York",
name="bar"`, second with `age=12, city="Berlin", name="bar"` and so on).
Similarly to the `args` list you can pass a list of parameters to scan as well,
i.e.

    $ ./run run foo --params "x=1,2,4 y=5,6"

computes all combinations of `x` and `y`.


## Dependencies

Besides the Python standard library, the `run` script requires

* daiquiri for logging setup
* marshmallow for loading and validation of runner descriptions
