# Team 7
# Bob Souwer & Alejandro salazar
# 16-01-2017

point_intersect <- function(points, buffer) {
  #Intersect one file with the other
  intersections <- gIntersection(points, industrial_buffer, byid = T,
                                 id=as.character(points$osm_id))
  #Make sure that intersected file still has its attribute names
  int_places <- points[points$osm_id == rownames(intersections@coords),]
  return(int_places)
}