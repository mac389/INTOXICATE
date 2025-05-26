__Current Goal__: Make database of synthetic patients. 

__Limitations of Current Approach__: `./src/for_model/create_synthetic_patient.py` uses random probability distributions. This was useful for proof of concept, but is not realistic. For example, the probability of someone having cirrhosis is not 50%. If `len(x)=n`, where `x` is the number of values that the feature _cirrhosis_ can take, then the probability of `cirrhosis==Yes` is `1/n`. This is not realistic. The probability of cirrhosis is about 0.2% in the general population, and about 20% in patients with chronic liver disease.

The diagnostic criteria for cirrhosis are: 
1. Platelet count < 150,000 (if no other explanation) 
1. Albumin < 3.5 mg/dL (if no albuminuria, malnutrition) & AST > ALT. 
1. INR > 1.2.

The ideal thing is to __find the prevalence of cirrhosis in the poisoned population__. This is not the same as the prevalence in the general population or in patients who develop acute liver failure after poisoning. 

It's important to ground the model distributions (for cirrhosis, respiratory failure, etc), because any model can generate unrealistic predictions if given data unrelated to its training data. __Make a table, there may be multiple sources of values for each feature.__

__Systems Architeture__: I originally used a MongoDB. Once I figure out how to deploy a remote one, we can write to that. In the meantime, use a JSON array. 
