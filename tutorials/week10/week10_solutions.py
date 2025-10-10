

##############
# Exercise 1 #
##############

### BEGIN SOLUTION
i = 0
max_components = len(pca.explained_variance_ratio_)

explained_variance = 0
while explained_variance < 0.9 and i < max_components:
    explained_variance += pca.explained_variance_ratio_[i]
    i += 1
    
print(f'{i} components explain {round(explained_variance * 100,2)}% of the variation in our data.')
### END SOLUTION


##############
# Exercise 2 #
##############

### BEGIN SOLUTION
reducer = MDS(n_components=2, normalized_stress='auto')
result = reducer.fit_transform(log_expression.values.T)
result_df = pd.DataFrame(result, index=input_df.index.to_list())
plot_two_dimensions(result_df, meta, 'tissue')
plot_two_dimensions(result_df, meta, 'development')
### END SOLUTION


##############
# Exercise 3 #
##############

### BEGIN SOLUTION
reducer = TSNE(n_components=2, perplexity=7) # try with perplexity 20, 60
result = reducer.fit_transform(log_expression.values.T)
result_df = pd.DataFrame(result, index=input_df.index.to_list())
plot_two_dimensions(result_df, meta, 'tissue')
plot_two_dimensions(result_df, meta, 'development')
### END SOLUTION


##############
# Exercise 4 #
##############

### BEGIN SOLUTION
reducer = umap.UMAP(n_components=2, n_neighbors=8)  # try with different n_neighbors eg 4, 10
result = reducer.fit_transform(log_expression.values.T)
result_df = pd.DataFrame(result, index=input_df.index.to_list())
plot_two_dimensions(result_df, meta, 'tissue')
plot_two_dimensions(result_df, meta, 'development')
### END SOLUTION


#############
# Extension #
#############

### BEGIN SOLUTION
# LDA with development labels
reducer = LinearDiscriminantAnalysis(n_components=2)
result = reducer.fit_transform(log_expression.T, meta['development'])
result_df = pd.DataFrame(result, index=input_df.index.to_list())
plot_two_dimensions(result_df, meta, 'development')
plot_two_dimensions(result_df, meta, 'tissue')

# LDA with tissue labels
reducer = LinearDiscriminantAnalysis(n_components=2)
result = reducer.fit_transform(log_expression.T, meta['tissue'])
result_df = pd.DataFrame(result, index=input_df.index.to_list())
plot_two_dimensions(result_df, meta, 'tissue')
plot_two_dimensions(result_df, meta, 'development')
### END SOLUTION