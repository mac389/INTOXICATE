**Exposure Category**.	The categories available are limiting. Exposures within our data set that do not fit into current categories include:

1. Fentanyl is a street drug and analgesic. We designated it as street drug because fentanyl is not an outpatient medication. 
2. Methadone doesn’t fit within the Brandenburg categories, which lack an opioid category. We designated it “street drug”.

**Respiratory Insufficiency**. We selected _Yes_ if the patient required any external support in the ED, for example intubation or nasal cannula. It's not clear how long the patient needs to recieve the support. 

**Dysrhythmia**. We included the expected atrial, ventricular and supraventricular dysrhythmias. We used thet definitions of tachycardia as a pulse greaeter than 100 bpm and bradycardia as less than 40 bpm. We included bundle branch blocks. We did not include STEMIs. 

**Actual Disposition**.
-	We used three categories: GMF, ICU, and Discharge.
-	SDU = ICU
-	Brandenburg's categories of ICU or not did not consisder discharge (or leaving against medical advice)[^1], nor transfers between ICU/SDU and GMF.
-	The data set for NYACP had no transfers after admission. We had one patient who left AMA whom we classified them as “Discharge”.

**Pulse, SBP, GCS**.
-	We used the initial ED values. 

  [^1]: One should include those who leave against AMA because they might come back and to reduce bias in population for estimating the model coefficients.
