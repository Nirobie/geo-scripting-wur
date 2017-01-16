# Team 7
# Bob Souwer & Alejandro salazar
# 16-01-2017

buffer_type <- function(dataset, type, buffer_width) {
  #Subsets the dataset using the type parameter
  selected <- dataset[dataset$type == type,]
  #Creates a buffer around the selected data
  buffered <- gBuffer(selected, width = buffer_width, byid = TRUE)
  #Returns the created buffer
  return(buffered)
}

