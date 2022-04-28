# Link prediction

## Conversion 
Plingo to ProbLog format
```
export PLINGO_DIR=plingo/instances
export PROBLOG_DIR=problog/instances

for instance in $(ls $PLINGO_DIR)
do
    python convert_plingo_to_other.py -t problog -f $PLINGO_DIR/$instance -o $PROBLOG_DIR/${instance/%.lp/.pl}
done 
```

Plingo to azreasoners format
```
export PLINGO_DIR=plingo/instances
export AZ_DIR=azreasoners/instances

for instance in $(ls $PLINGO_DIR)
do
    python convert_plingo_to_other.py -t az -f $PLINGO_DIR/$instance -o $AZ_DIR/$instance
done
```

## Running the benchmark
### Plingo
#### MAP estimate

```
cd plingo/
plingo encoding.lp instances/$instance 
```
#### Query
Runs balanced query mode.
`NUM_MODELS=5` determines 10 models in total.
```
cd plingo/
export NUM_MODELS=5
plingo encoding.lp query.lp $instance --opt-enum -q1 -b${NUM_MODELS}
```
### ProbLog
https://problog.readthedocs.io/en/latest/index.html
The `mpe` mode currently does not seem to work on macOS with pip install. Might work when compiling (?) (https://github.com/ML-KULeuven/problog/issues/65)
#### MAP estimate
```
cd problog/
problog mpe $(cat instances/$instance)
```

#### Query exact
```
cd problog/
problog instances/$instance
````

#### Query sample
Runs ProbLog sampling mode
```
cd problog/
export NUM_SAMPLES=10
problog sample instances/$instance --estimate -N $NUM_SAMPLES
```

### azreasoners
https://github.com/azreasoners/lpmln
#### MAP estimate
`--verbosity 1` prints the correct runtime

```
cd azreasoners/
lpmln-infer encoding.lp instances/$instance --verbosity 1
```

#### Query
No approxiomation in azreasoners.
