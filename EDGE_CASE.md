# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
POST /students — Creates a student with name, course, optionally mark.
GET /stats — Return count, average, min, max of all student marks.

mark is optional when creating students so some students may not have a mark but stats want us to find the count, average, min, max of all student marks and doesnt specify what to do when students have no marks

2) How you have accounted for this in your implementation
if there is no mark for a student then we dont count that student when calculating stats
