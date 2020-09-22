## Batsim Evaluation of the BEE Scheduler

First clone or download the BEE\_private repo into the root directory. Follow
the setup instructions to get the dependencies installed. Install `pybatsim`
with pip into the venv.

In order to simulate the scheduling environment we must start two separate
process, one for Batsim and the other for the BEE Scheduler interface.

To start Batsim run in one terminal:

```
./run-batsim.sh
```

Then to run the BEE Scheduler interface enter the venv and then run this
command in another terminal:

```
pybatsim beeSched.py
```
