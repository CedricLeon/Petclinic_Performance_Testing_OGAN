# Spring PetClinic REST API Performance Testing using Online GAN

This repository uses the **stgem** library ([here](https://gitlab.abo.fi/svv/stgem-release)) and its Online Generative Adversarial Network (OGAN) algorithm to realize Performance tests of a REST API version of the Spring Petclinic ([here](https://github.com/spring-petclinic/spring-petclinic-rest)).







## Adapter function

The final goal being the performance testing of this simple REST API using Online GAN, a function managing interactions between the 2 entities is required.

The GAN generates numbers $\in [0;1]$ and we want this number to be responsible for a certain endpoint call.

#### Homogeneous adapter

In this method we will simply segment all the available endpoints in equally sized intervals.

For instance in the `v1.0`:

-  There is only 4 possible endpoints (**GET**, **PUT**, **PATCH** or **DELETE**) for the unique Resource **Client** of the API.
- Segmentation example: allow **GET** to $[0;0.25]$, **PUT** to $[0.25;0.5]$, **PATCH** to $[0.5;0.75]$ and **DELETE** to $[0,75;1]$.
- Therefore, if the GAN generates $0.7314$, this corresponds to a **PATCH** call.

###### Now what arguments will the call use?

The easy cases are **GET** and **DELETE**, there is 2 possible outcomes: the resource we want access to exist or not. The 2 cases are interesting but we imagine from a performance point of view that the second one will not really be complicated: once the API had figured out the resource is not in the database the only action left is to return an error message and the corresponding status code. So, we may want the GAN to try more calls with existing resources. This can be "stupidly" done by just looking at the database size and calling an **id** such as $id \in [0..db_{size}-1]$ .

On the other side, **PUT** and **PATCH** are http requests which need a body. This means we need to give more arguments to the request (in a JSON format for instance). When talking about strings we don't really care about the meaning of that string and we can generate it randomly, same an integer number. But, we care about the number of arguments and the type off each argument, for instance in `v1.0` the **Client PUT** endpoint had 3 required arguments:

- **name**: String(100)
- **gender**: String(100)
- **age**: Integer

Using a dictionary specifying for each resource the available endpoints, their number of arguments and their types. We can even imagine that this dictionary gives an example and we only use that example for the requests instead of generating randomly the strings and numbers.

But this "simple" method will not differentiate $0.7314$ from $0.532$ for example, both numbers are in the **PATCH** segment, this would end with the same endpoint call.

#### Resource separated adapter

This method would work on the same principle but would be more general and "precise". If the API owns several resources, we want to test every ones of them. The first adapter does not differentiate the **Client** **GET** endpoint from a potential **Manufacturer** **GET** endpoint.

The idea would be to first divide our unitty segment into further segments of length $\frac{1}{Nb_{resource}}$ and then to divide each of this sub-segments into smaller segments, one for each endpoint of the corresponding endpoint.

We can even push the idea further and that these sub-segments (Sized $\frac{1}{Nb_{resource} \times 4}$ if we consider each resource has the same amount of endpoints and that we stay with the 4 basic ones) could be further divided depending of type of status code it will generate. For instance, we could incorporate in the dictionary 2 different **Client GET** call, one with a valid **id** (and therefore a status code of 200), and another with a non-existing **id** (==status code of 404?==).

202?



## "Build" the repository

If you want to clone and run this repository, make sure you have a Python Version higher than 3.6 (use of *fStrings*).

````bash
# "Build"
git clone https://github.com/CedricLeon/RESTAPITest.git
pip3 install -r requirements.txt
````

````bash
# In one shell: Run the API
python3 main.py
````

````bash
# In another shell: call the test file interacting with the API
python3 test.py
````

You can also create a **virtualenv** to install the dependences and run the API.
