##### db_encoded.csv :

Each sequences take up 4 rows of dummy data, by 130 columns. The 4 rows are arranged, from top to bottom, with round brackets, square brackets, curly brackets, and angle brackets. For a single entity, the top row is index 0, and the bottommost row is index 3. The scale is discrete with values [+1, 0, -1]. Where open-bracket is +1, close-braket is -1, dots is +0.

##### kt_encoded.csv :

Each sequences take up 6 rows of dummy data, by 130 columns, to represent 7 types. The rows are arranged, from top to bottom, holding the values of 'X', 'S', 'M', 'I', 'H', 'E', and 'B' respectivelly, with the last row 'B' being excluded as it intercept with all the other categories together. For a single entity, the top row is index 0, and the bottommost row is index 5. The scale is discrete with values [0, 1].

##### lp_encoded.csv :

Each sequences represent a single row, by 130 columns, to represent 2 types. The scale is binary with value [0, 1]. Where '1' represent a 'K', while '0' represent a 'N'.

##### nt_encoded.csv :

Each sequences take up 3 rows of dummy data, by 14 columns, to represent 4 types. The rows are arranged, from top to bottom, holding the values of 'G', 'C', 'T' and 'A' respectivelly, with the last row 'A' being excluded as it intercept with all the other categories together. The scale is discrete with values [0, 1]. The 14 columns are to represents only the variation and exclude redondancy between all sequences to simplify the ML model.
