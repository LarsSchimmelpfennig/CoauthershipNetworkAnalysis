# Co-authership Network Analysis

A Co-authorship network contains authors as nodes and collaboration on the same paper as edges. The analysis of these networks is often used to explore the development of a field and guide future collaboration. My project focuses on how authors specializing in different topics within a field are distributed in terms of collaboration. Do authors with the same interests collaborate the most? Is there polarization in the distribution of these authors?

To capture what topics each author focuses on I have used a deep learning Word2Vec model I trained on all abstracts from 1980 to 2022 in the Web of Science CORE dataset. During training this model creates word vectors based on the context each word appears in. These word vectors can be combined to capture more complex meaning and the cosine similairty between two word vectors gives a value from -1 to 1 depending on how similar these word vectors are. 

I can combine word vectors for all the text in the title and keywords for each paper by an author. This gives an author vector that represents all the work an author has contributed towards within a specifc field.

When we measure the cosine similarity between the all author vectors and the average of all author vectors we get the following histogram. This gives approximelty a left-skewed normal distribution with the mean cosine similarity near .925. This is to be expected as few authors will be significantly different from the average author vector. This distribution was created from the Foldamer Co-authorship network. Other fields of research will have varying means and standard deviations depending on how varied the topics researched are.

<div align="center">
  <img src="https://github.com/LarsSchimmelpfennig/CoauthershipNetworkAnalysis/assets/91089724/ee188d0f-1de4-42d1-b8ce-3b8e2540a289" alt="Image" width="50%" />
</div>

For our analysis of these networks I will focus on the following metrics. Modularity is the proportion of edges from nodes in a cluster that connect to other nodes in the same cluster. Here clusters are assigned to maximize modularity. An increase in modularity represents an increase in edge density within a cluster. Next we will use the average distance between neighboring word vectors. This is computed using the value described in the histogram and will help tell us if authors with similar interests are working together. Lastly I have included homophily which measures the proportion of neighboring nodes with a score within some threshold. This is a metric for network polarization where high homophily values represent a higher degree of polarization. I have chosen to use the standard deviation of scores/2 as a threshold.

<div align="center">
  <img src="https://github.com/LarsSchimmelpfennig/CoauthershipNetworkAnalysis/assets/91089724/7d562964-7b32-47cd-94c9-6efe17c76035" alt="Image" width="50%" />
</div>


| Header 1 | Header 2 | Header 3 |
|:----------|:----------:|----------:|
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
| Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 |
| Row 3, Col 1 | Row 3, Col 2 | Row 3, Col 3 |











# Future Work

<li>Instead of generating these author vectors through the text in their publications I can instead train a new Word2Vec model with the authors of each paper directly. Authors that appear in the same papers will then have a higher cosine similarity. To attempt this, I would need to address Author Name Disambiguation (AND) which is a complex problem as many authors dont publish under a consistent spelling and many share the same name.</li>

<li>I can also use the text of all papers written by the authors in a network when creating these author vectors, however, this would also require work on AND.</li> 
