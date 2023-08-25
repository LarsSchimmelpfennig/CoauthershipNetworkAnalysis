# Co-authorship Network Analysis

A Co-authorship network contains authors as nodes and collaboration on the same paper as edges. The analysis of these networks is often used to explore the development of a field and guide future collaboration. My project focuses on how authors specializing in different topics within a field are distributed. Do authors with the same interests collaborate the most? Is there polarization in the distribution of these authors?

To capture what topics each author focuses on I have used a deep learning Word2Vec model I trained on all abstracts from 1980 to 2022 in the Web of Science CORE dataset. During training this model creates word vectors based on the context each word appears in. These word vectors can be combined to capture more complex meaning and the cosine similarity between two word vectors gives a value from -1 to 1 depending on how similar these word vectors are. 

I can combine word vectors for all the text in the title and keywords for each paper by an author. This gives an author vector that represents all the work an author has contributed towards within a specific field. When we measure the cosine similarity between the author vectors and the average of all author vectors we get the following network for the field of foldamers.

![foldamer_transparent_4](https://github.com/LarsSchimmelpfennig/CoauthorshipNetworkAnalysis/assets/91089724/3a5ba29c-bbb3-4564-b103-346bb7c3a9bb)

This gives approximately a left-skewed normal distribution with the mean cosine similarity of .931. This is to be expected as few authors will be significantly different from the average author vector. This distribution was created from the foldamers Co-authorship network. Other fields of research will have varying means and standard deviations depending on how varied the topics researched are.

<div align="center">
  <img src="https://github.com/LarsSchimmelpfennig/CoauthershipNetworkAnalysis/assets/91089724/ee188d0f-1de4-42d1-b8ce-3b8e2540a289" alt="Image" width="60%" />
</div>

For this analysis of these networks I will focus on the following metrics: Modularity is the proportion of edges from nodes in a cluster that connect to other nodes in the same cluster. Here clusters are assigned to maximize modularity. An increase in modularity represents an increase in edge density within a cluster. Next we will use the average cosine similarity between neighboring author vectors. Lastly I have included homophily which measures the proportion of neighboring nodes with a cosine similairty above some threshold. I set this threshold to be one minus half the standard deviation of author vectors. This is a metric for network polarization where high homophily values represent a higher degree of polarization.

<div align="center">
  <img src="https://github.com/LarsSchimmelpfennig/CoauthorshipNetworkAnalysis/assets/91089724/8a60bd40-a61f-498a-8fa6-f8d728ac92b0" alt="Image" width="60%" />
</div>

To measure the significance of association between curves I can perform a linear regression using the SciPy stats module.

<div align="center">
  <img src="https://github.com/LarsSchimmelpfennig/CoauthorshipNetworkAnalysis/assets/91089724/6dc325f7-2eb0-4b7c-91c9-a2514deac967" alt="Image" width="60%" />
</div>

## Regression results 

### Amelanotic Melanoma

| Metrics                                      | Slope | R-Squared | P-Value |
|:--------------------------------------------:|:-----:|:---------:|:-------:|
| modularity, cosine similarity of neighbors  | -0.033 | 0.857    | 9.61e-8  |
| modularity, homophily                       | -0.297 | 0.242    | 0.045    |
| homophily, cosine similarity of neighbors   | 11.44  | 0.463    | 0.002    |

### Foldamers

| Metrics                                      | Slope | R-Squared | P-Value |
|:--------------------------------------------:|:-----:|:---------:|:-------:|
| modularity, cosine similarity of neighbors  | -0.008 | 0.103    | 0.125    |
| modularity, homophily                       | 0.393  | 0.939    | 7.42e-15 |
| homophily, cosine similarity of neighbors   | -3.34  | 0.043    | 0.327    |

### Spliceosome

| Metrics                                      | Slope | R-Squared | P-Value |
|:--------------------------------------------:|:-----:|:---------:|:-------:|
| modularity, cosine similarity of neighbors  | -0.031 | 0.161    | 0.052    |
| modularity, homophily                       | -0.399  | 0.121   | 0.095    |
| homophily, cosine similarity of neighbors   | -3.24  | 0.05     | 0.293    |



# Conclusion

It is very interesting that these different curves would share such similar features for some fields over time and not for others. For the first metric, modularity and cosine similarity of neighbors, as clusters of authors become more interconnected the distance between their author vectors increases. A significant p-value seems to suggest that dense clusters of authors are formed that are diversified. Collaborators may bring unique contributions without large overlap.


# Future Work

<li>Instead of generating these author vectors from the text in their publications I can instead train a new Word2Vec model with the authors of each paper directly. Authors that appear in the same papers will then have a higher cosine similarity. To attempt this, I would need to address Author Name Disambiguation (AND) which is a complex problem as many authors don't publish under a consistent spelling and many share the same name.</li>

<li>I can also use the text of all papers written by the authors in a network (instead of those just within a specific field) when creating these author vectors, however, this would also require work on AND.</li> 
