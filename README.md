# Instructions

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
1. Edit `start_me.bat` to reflect location of miniconda, usually in the home directory. Line 7 should look like:

```
CALL C:\Users\<USERNAME>\miniconda3\Scripts\activate.bat C:\Users\<USERNAME>\miniconda3
```
3. Clone repo, install python, install pip libraries

```
git clone https://github.com/pomkos/dynamic_biking
cd dynamic_biking

conda install python=3.8
pip install -r requirements.txt
```

4. Launch script by double clicking on `start_me.bat`
