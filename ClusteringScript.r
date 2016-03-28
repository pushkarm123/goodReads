setwd('d:/web mining/project')
books <- read.csv('d:/Web Mining/Project/csv_files/book_data.csv')
books <- books[1:nrow(books)-1,] 

colnames(books)
books$published
books_training_set <- books[,20:43]

colnames(books_training_set)

#books_training_set_mut1<- books_training_set[is.na(books_training_set[,'books.publication_year']) == F,] 

#books_training_set_mut1$books.publication_year


#dim(books_training_set)
#sum(is.na(books_training_set))

#head(books_training_set_mut1)

#books_training_set_mut1 <- books_training_set_mut1[complete.cases(books_training_set_mut1),]

#sum(is.na(books_training_set_mut1))
-------------------------------------------------------------------------
#dim(books_training_set_mut1)
#books_training_data <- books_training_set_mut1[,]


sum(is.na(books_training_data))
dim(books_training_set)
class(books_training_set_mut1[1,19])
-------------------------------------------------------------------------
#indx <- sapply(books_training_set_mut1,is.)
#sum(indx)
#books_training_set_mut1[indx] <- lapply(books_training_set_mut1[indx], 
#                                    function(x) as.numeric(as.character(x)))

# lapply(training_data, class)

# sum(is.na(scale(books_training_set_mut1)))

 -------------------------------------------------------------------------------- 

#books_training_set_mut1[]
 
#max(books_training_set_mut1[]) 
 
x <- scale(books_training_set)    
sum(is.na(x))
#sum(is.na(x))
x
dim(x)
sum(is.infinite(x))


training_data <- as.matrix(x)
sum(is.na(training_data))



#books_training_set_mut1[is.nan(training_data),]

#sum(is.na(training_data))
#books_training_set[786,1]

#books_training_data[786,1]

require(kohonen)
som_grid <- somgrid(xdim = 20, ydim=20, topo="hexagonal")
som_model <- som(data = training_data, grid = som_grid,rlen = 1000, n.hood = "circular" )
books_training_data[1,1]
plot(som_model, type="count")
som_model
?som
som()

books_training_data

som.wines <- som(scale(books_training_data), grid = somgrid(5, 5, "rectangular"))

books_training_data[1,]

books.to_cluster
length(books$isbn)
sum(is.na(books_training_set))

kc <- kmeans(x, 10)
kc
plot(kc)
x$cluster_no = kc$cluster 
training_data$cluster_no

clustered_book_set <- data.frame(books$isbn,books$title,kc$cluster)

clustered_book_set$kc.cluster == 1
clustered_book_set[clustered_book_set$kc.cluster == 1,"books.title"]

books$cluster_number <- kc$cluster


write.csv(books,"clustered_books.csv")
