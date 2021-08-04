# BYOM_Tableau

This page includes the dataset, code, and Tableau visualization for real-world business problem to find optimum real-estate investment strategy. Solving this problem requires a dynamic interaction with multiple machine learning models. The models are built outside of Tableau with Python, and then Tableau Analytics Extensions API had been used as a deployment platform to mingle the models together and make it accessible through Tableau platforms. Hence, the business users will be able to interact with these models in real time. 


The required steps to get the Python code and Tableau workbook run successfully:
1. Install [TabPy](https://github.com/tableau/TabPy) package: `pip install TabPy`
2. Install [knapsack solver](https://github.com/Alieladi/knapsack-pip) package: `pip install knapsack-pip`
3. Modify the deployment part of Python code: `client = Client('http://localhost:9004/')` 
   1. The URL and port are where the Tableau-Python-Server process has been started - more info can be found in the [Starting TabPy](https://github.com/tableau/TabPy/blob/master/docs/server-install.md#starting-tabpy) section of the documentation.
   2. If TabPy is configured with the authentication feature on, client code has to specify the credentials to use during model deployment with the set_credentials call for a client `client.set_credentials('username', 'P@ssw0rd')')`
4. Run the Python code while TabPy is up and running. 
5. Adjustment the configuration of Tableau workbook according to your TabPy serevr info.
