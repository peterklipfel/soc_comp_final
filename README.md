soc_comp_final
==============

final project for social computing

## On Ubuntu


We are using pip + venv.. so, make sure you run

    sudo apt-get install python-virtualenv python-pip git build-essential python-setuptools python-dev

and for the numpy & scipy dependencies 
    
    sudo apt-get install libblas-dev liblapack-dev gfortran

and then to install the dependencies

    virtualenv --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

