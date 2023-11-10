## This is an operation research project
authors: Yang Yuzi, Feng Jixuan, Chen Nuo from Zhejiang University.

## Files:
`application.py`	        application program for executing simulation, handlers for sales and logistics\
`topology.py`    		generates network of stores, plants, warehouses and truck delivery\
`post_process.py`	        miscellaneous functions for plotting\
`visualization.py`        module for interactive data visualization (not tested on DeepThought) \
`store_info.csv`          contains input for topology generation

## To run the program
### part 1
In path `./OR-homework/`, run `python parameter_study.py` to study trucks and minimum safety stock percent. 

When you study a parameter, please uncomment corresponding block. This part will generate some figures showing the baseline simulation result.

the two block are written as:
> block 1\
=========== study trucks ===========\
>......\
>=========== study trucks ===========

>block2\
>=========== study minmum percent ===========\
>......\
>=========== study minmum percent ===========

### part2
In path `./OR-homework/find_opt_parameter/`, run 'python main.py' to study parameter lambda. This part will generate the grid search result added in the file `./find_opt_parameter/result.txt`.