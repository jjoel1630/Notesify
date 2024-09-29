from transformers import pipeline
from transformers import BartTokenizer
import openai
import os
import unicodedata
import re
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

def normalize_text(text):
    # Normalize Unicode characters to their closest ASCII representation
    text = unicodedata.normalize('NFKD', text)
    replacements = {
        '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5',
        '₆': '6', '₇': '7', '₈': '8', '₉': '9', '₀': '0',
        '…': 'and so on', '−': 'minus', '+': 'plus', '=': 'equals',
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    # Remove any other special characters not replaced above
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!-]', '', text)
    text = text.replace("\n", " ").strip()

    return text

def condense(text, max_words):
    CHAR_PER_WORDS = 4.7
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    normalized_article = normalize_text(text)
    
    max_char = int(max_words * CHAR_PER_WORDS)
    proportion_reduction = max_char / len(text)
    tokenized_text = tokenizer(text)
    
    max_tokens = int(len(tokenized_text['input_ids']) * proportion_reduction)
    
    # print("proportion_reduction")
    # print(proportion_reduction)
    
    # print("tokenized_text")
    # print(tokenized_text)
    
    # print("max_tokens")
    # print(max_tokens)
    # (current) expect / current = expect
    
    WORD_PER_TOKEN = 0.67  # This is a rough average; you may want to adjust it based on your specific data
    token_count = int(max_char / WORD_PER_TOKEN)  # Convert words to tokens

    # Define max and min lengths based on token counts
    max_length = min(token_count, 1024)  # Set to max token limit of the model
    min_length = int(max_length * 0.4)  # Minimum is 40% of max_length


    MAX_INPUT_LENGTH = 1024
    chunks = [normalized_article[i:i + MAX_INPUT_LENGTH] for i in range(0, len(normalized_article), MAX_INPUT_LENGTH)]
    
    summaries = []
    gpt_summaries = []
    for chunk in chunks:
        try:
            # print("chunk pre-GPT")
            # print(chunk)
            
            tokenized_text = tokenizer(chunk)
            max_tokens = int(len(tokenized_text['input_ids']) * proportion_reduction)
            # print("max_tokens")
            # print(max_tokens)
            
            chunk_summary = summarizer(chunk, max_length=max_tokens, min_length=int(0.4 * max_tokens), do_sample=False)
            # print("CONDENSED")
            # print(chunk_summary[0]['summary_text'])
            
            spell_checked_chunk = gpt_call("You are an assistant that completes spell-checking.", "Write out the gramatically correct form of: " + chunk_summary[0]['summary_text'] + ". Don't state whether changes are needed or not.")
            summaries.append(spell_checked_chunk)
            # print("spell_checked_chunk")
            # print(spell_checked_chunk)
            
        except Exception as e:
            print(f"An error occurred while summarizing chunk: {e}")
    
    condensed_summary = " ".join(summaries)
    
    # print("condensed_summary")
    # print(condensed_summary)
    
    return condensed_summary

def gpt_call(system_prompt, user_prompt):
    openai.api_key = api_key
    
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    output = response['choices'][0]['message']['content']
    
    return output

def convertToScript(text):
    openai.api_key = api_key
    max_length = len(text.split())
    max_tokens = 1000
    chunks = [text[i:i + max_tokens] for i in range(0, len(text), max_tokens)]

    script = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that converts notes to a script."},
                {"role": "user", "content": f"Reword the following text to be a short script that is less than the length of the input, and replace special characters with English equivalent: {chunk}"}
            ]
        )
        output = response['choices'][0]['message']['content']
        if len(output.split()) > max_length:
            output = " ".join(output.split()[:max_length])  # Trim to max length
        script.append(output)

    full_script = " ".join(script)
    return full_script

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

if __name__ == "__main__":
    # The following arguments will be passed as paramters
    text = '''
        Definitions:
        A 'Linear equation' is an equation like a1x1 + a2x2 + ... + anxn = b, where ‘b’ is the solution obtained by ordering coefficients and variables.

        A 'System of linear equations' is a collection of various linear equations.

        'Solution of a system' (s1, s2, ..., sn) refers to an array of numbers that make every equation true when the s values are replaced by the x variables.

        'Solution set' is all potential solutions for a linear system.

        'Equivalent linear systems' are two linear systems sharing the same solution set.

        'Consistent system' is defined by one or many indefinite solutions.

        'Inconsistent system' exists when for a specific input, there's no solution.

        'Existence' questions if a solution set exists.

        'Uniqueness' asks if any existing solution is unique or multiple.

        In summary:
        A system of linear equations has either no solution, one solution, or infinite solutions.

        'Matrix notation' is a rectangular array containing linear system data.

        Here's an example system:
        1x1 - 2x2 + x3 = 0
        0x1 + 2x2 - 8x3 = 8
        5x1 + 0x" "The equation, five times the third variable is subtracted from two, equals ten. Regarding matrices, a coefficient matrix precedes the augmented matrix. The size of any matrix depends on its rows (m), and columns (n), highlighted as m by n. 

        In row reduction, 'Replacement' denotes eliminating elements by comparing and adjusting rows. 'Interchange' involves swapping rows and 'Scaling' makes the leading entry one. This operation's goal is to form an echelon or RREF, showcasing a triangle of zeros.

        The main points of Section 1.2 are: 

        - Non-zero row/column: A row or column with minimum one nonzero entry
        - Zero row/column: A row or column entirely zero
        - Leading entry: The first nonzero entry in each row

        Row reduced echelon form (RREF) simplifies matrices to depict potential solution sets, and each matrix has one unique RREF. 

        The pivot position, located where the leading entry is one in RREF, has a central role. The column with a pivot position is the pivot column. Basic or leading variables correspond to a pivot and provide the precise value for a solution set while free variables..." SCRIPT:

        In a consistent linear system, columns with no corresponding pivots can be assigned any value.

        If the number of rows exceeds the number of columns, predomes the overdetermined system. This kind of linear equations system can be consistent and have a unique solution.

        In contrast, if the number of columns outweighs the number of rows, it substantiates the underdetermined system. This type of linear system cannot have a unique solution and often presents a free variable. If consistent, it will display infinite solutions. However, if it's inconsistent, it will show no solution.

        Keynotes revolve around the Echelon Form of a Matrix's three distinct properties:
        1. Zero rows settle at the bottom.
        2. Each relevant row entry is right-sided to leading entries above it, if any.
        3. All entries under a leading entry are zero.

        The RREF maintains leading entries as one's, zero's placed above and beneath each leading one. If a matrix is neither in echelon form nor RREF, additional row reduction is necessary.

        Lastly, the uniqueness of the RREF specifies that every matrix is a row. A matrix corresponds to a single reduced echelon form. Inconsistent systems equate to empty solutions.

        The "Existence and Uniqueness Theorem" states that a linear system is consistent exclusively if the augmented matrix's farthest right column isn't a pivot column. If the system is consistent, the solutions are either unique with no free variables, or infinitely many with at least a single free variable.

        Jumping to the topic of Midterm 2, which reviews Midterm 1 guide, studying Inverse Matrix under section 2.2 is needed. Here are key concepts:

        - An "Invertible Matrix" is an n x n matrix A.
        - "Inverse of a Matrix" is A^(-1).
        - A matrix is "Singular" if it isn’t invertible.
        - "Determinant of a 2x2 matrix" is computed as ad - bc.
        - "Elementary Matrix (E)" is a matrix derived from performing a single row operation on an identity matrix, which is also invertible, its inverse is another E-type, taking E back to I. "Elementary matrices are all invertible. We term them as row equivalent matrices when they can transition into one another via a sequence of elementary row functions. Understand that invertible also implies nonsingular and non-invertible denotes singular. 

        Let's say we have a two by two matrix, its invertibility relies on the equation 'ad - bc' equalling zero; if so, the matrix isn't invertible. The equation Ax=b can be recast using inverse values if A is nonsingular. You can employ row reduction techniques to decode Ax=b. 

        If you have every number in Rn, x equates to the unique solution A-inverse b. Nonsingular matrices lack free variables, thus having unique solutions. Beware, the product of n by n invertible matrices remains invertible. The inverse of a product equals the product of their inverses in reverse order. 

        Performing an elementary row operation on an m by n matrix A results in a matrix labelled as EA. You might wonder, what if A undergoes multiple elementary row operations? 

        For finding the inverse, simultaneously row reduce matrix A and the Identity Matrix. And there you have your inverse." "I" refers to "A-1". A matrix is only invertible if its identity is row equivalent, with pivots in every row and column. 

        In terms of Invertible Matrices, a Linear Transformation is a preserved mapping between two vector spaces, E.g. Rn. An invertible Linear Transformation is a transformation where, for example, T:Rn -> Rn, another transformation exists, S: Rn -> Rn, that allows S(T(x)) = x and T(S(x)) = x for all x within Rn, which equates to saying Ix = (A-1Ax).

        Here's the Invertible Matrix Theorem (IMT). Presume A and B are square matrices. If AB = I, A and B are invertible. Hence, B equates to A-1 and vice versa. To determine if a linear transformation is invertible, let matrix A represent the transformation. If A is invertible, the transformation will be too. 

        In the case of Partitioned Matrices, a Partitioned Matrix is a fractionally divided Matrix. "Block Diagonal Matrix is a partitioned matrix with only main diagonal blocks bearing values while others contain zeros. It's invertible exclusively if the main diagonal blocks are.

        To add or scale two partitioned matrices - A and B, ensure they're identical in size and partition, then proceed block by block. 

        Multiplying two partitioned matrices? Simply follow standard multiplication rules. The column count in Partition A should match the row count in Partition B. For example, (2 x 2) and (2 x 1) yields a (2 x 1) matrix.

        Moving on to Matrix Factorizations. Factorization implies expressing a matrix as a product of numerous matrices. Swapping rows when row reducing is known as row interchanges.

        Lower triangular matrix? All entries above the main diagonal are zeros. On the contrary, in an upper triangular matrix, entries below the main diagonal are zeros." "LU Factorization Short Script

        LU Factorization's algorithm can be simplified as follows: 

        1. Convert matrix A into echelon form, U, through a series of row replacements. 

        2. Match entries in L so the same sequence of row operations simplifies L to I.

        LU Factorization is used for its efficiency in solving sequences of equations with identical coefficient matrices (Ax = b1, Ax = b2, ..., Ax = bn), rather than row reducing equations each time. If the m x n matrix A can be row reduced to echelon form with no row swaps, then:

        - L is an m x m lower triangular matrix with ones on the main diagonal,
        - U is an m x n echelon form of A.

        A = LU allows to reformat Ax = b equation into: L(Ux) = b. 

        To obtain U, reduce A to echelon form by adding row multiples to rows beneath it. To get L, repeat the row replacements applied on A during echelon form. In essence, it's all about finding the elements." Below is a condensed script:

        "Start by finding the elementary matrices that convert A to U. Now, switch the signs and insert them into the suitable places in the m x m identity matrix.

        We then replace the 0s beneath the main diagonal with row replacement coefficients. Basically, after identifying all the elementary matrices, invert them. 

        We'll also leverage the LU Decomposition by first building A = LU and solving Ax = LUx = b through two steps. 

        Step one, forward solve for y in Ly = b, changing the rows beneath using the rows above. Step two, backwards solve for x in Ux = y, modifying the rows above using the rows beneath.

        Now in Sect 2.6, The Leontief Input-Output Model, we have key definitions. We have the 'Production vector' in Rn or 'x', outlining the output of each industry for one annum. 'Final demand vector' or 'd', enumerates the value of consumer-focused goods and services. 'Intermediate demand' or 'Cx', represents the demand for goods and services needed by producers for their own production. For instance, the electricity sector's need for inputs from..." Here's a concise script representing your notes:

        Discuss the relationship between sectors and water. Discuss the consumption matrix (C) which represents inter-sectoral consumption percentages. Talk about column totals indicating the sum of entries in a column. 

        Mention the Leontief Input-Output Model with the equation: (I - C)x = d. Explain solving for 'x' (the production amount) using row reduction, resulting in: x = (I - C)-1 * d.

        Emphasize the economic ideal where a sector's column sum should be less than 1. A sector should use less than one unit of input to produce one unit of output.

        Define the output vector (x), where xi is the production volume by sector i. Dive into internal consumption (C) which, defined by ci,j, shows how sector i provides units to sector j, and vice versa.

        Finally, describe the consumption matrix (Cx), a sum of the columns representing each sector's total output per unit. Title: Economic Formulas and Computer Graphics Introduction

        Narrator: Let's introduce our economy to a demand vector equation, 'x = d.' Keep in mind, production needs intermediate demand from other sectors, evolving the equation into 'x = d + Cd + C^2d + C^3d + ….'

        This leads to our reformulated equation: '(I + C + C^2 + C^3)d.'

        To improve the accuracy, we aim to maximize 'm' in '(I - C)^-1,' adding as much intermediate demands as possible.

        Remember, these entries in the matrix '(I - C)^-1' help predict changes in production 'x' given changes in final demand 'd.' Hence the equation 'x = (I - C)^-1 * d.' Each column of '(I - C)^-1' shows the increased production each sector needs to meet a rise in the unit of final demand.

        Now, let's pivot to Computer Graphics Application. We must understand homogeneous coordinates - where each point '(x, y)' in R^2 is connected with '(x, y, 1)' on the R^3 plane, one unit above the xy-plane. Also crucial is the concept of composite transformation... "Today, we're going to discuss the multiplication of multiple basic transformations. To kick things off, let's focus on the importance of homogeneous coordinates. These are necessary because translations aren't considered linear transformations. But when we start talking about homogeneous coordinates, there's no need to fret - these are simply allowed to be scalars. For example: (3, 5, 1) is equivalent to (6, 10, 2). 

        When we change (x, y) to (x + h, y + k), we should remember that this type of translation can't be represented by a simple R2 matrix multiplication. Instead, it should be depicted as (x, y, 1) changing to (x + h, y + k, 1). 

        Linear transformations in R2 are written as partitioned matrices with homogeneous coordinates, where A is a 2x2 matrix. Considering composite transformations, the procedure entails adding more transformation matrices to the left of existing ones, with the first transformation always being the rightmost. 

        For 3D Homogeneous Coordinates, we write (X, Y, Z, H) as (x, y, z) if H does not equal zero.

        Now, switching gears to Subspaces of Rn, it's essential to understand its definitions: subset of Rn refers to any collection of vectors present in Rn, whereas a subspace of Rn is a subset H." Script:

        In RN, we have H which is a subspace with three properties: it includes the zero vector, and is closed under both addition and scalar multiplication. This subspace, H, can be described as the Span of several linearly independent vectors.

        We then consider the Matrix A, size m x n, which has a Column Space (Col A) and Null Space (Null A). Col A is a subspace of Rm spanned by the elements a1 , … , an and includes all pivot columns. Null A, on the other hand, is a subspace of Rn spanned by vectors x that satisfy the equation Ax = 0.

        There's also a Basis for the subspace H which is a linearly independent set in H that spans H. An important note to remember is that, unlike the Span, it does not contain the zero vector as it needs to remain linearly independent.

        For Rn, there's the Standard Basis, represented by {e1 , … , en}.

        A few key points to remember:
        - If v1 and v2 are in Rn and H equals Span of v1, v2, then H is a subspace of Rn, but only if v1 and v2 are included in Rn.
        - For any set of v1 to vp in Rn, all linear combinations of these elements also form a subspace of Rn. So, Span of v1 to vp equals the subspace spanned by v1 to vp. 
        - To determine if b is in the column space of A, synthesize it: "Is b in A?" "Is b a linear combination of A, hence within A's span? Does H represent a subspace in Rn, implying it possesses n linearly independent columns with no free variables? Let's contrast subspaces and bases: subspaces span {v1, ..., vn}, including the 0 vector, while bases are {v1, ..., vn}. To define a basis for column space A, the vector entries match the number of matrix A rows, with the number of vectors equalling the pivot columns. Scalar multiples and identity matrix columns can be included only if each column is pivotal in A.

        The column space can be found by reducing rows, which don't alter linear dependence relations. Pinpointing pivot columns helps in forming a basis/subspace using original matrix pivot columns. If all columns are linearly independent, elementary vectors form part of the column space as their combinations can create any given column." "Original Matrix
        - Identify free variables to determine Null Space.
        - Recast system in parametric vector form.
        - The null space is formed by the vectors from this process.

        Section 2.9: Dimension and Rank
        Terms
        - Coordinates: the weights used to map vectors to a point within vector span.
        - Coordinate Vector: empty.
        - Dimension of a Subspace (dim H): the count of vectors in a basis of H; dim{0} equals 0.
        - Rank of a Matrix A: both the dimension of the A's column space and the count of A's pivots.

        Important Points
        - Basis writing: each vector in H can be uniquely expressed as a linear combination of basis vectors.
        - A plane in R3 via 0 is 2D; 3x3 matrix A has two pivots.
        - A line in R2 via 0 is 1D; 2x2 Matrix A has a single pivot.
        - Any two base choices of a non-null subspace H share the same dimension: dim Rn equals n, dim(Col A) is the count of pivots, and dim(Null A) equals the count of free variables.
        - dim(Col A) equals rank A.
        - Rank Theorem: empty." "Script Format:

        Let's assume that matrix A has n columns.
        Then, the summation of rank A and dimension of Null A equates to n, or you could say the total of number of pivots and number of free variables equals the number of columns.

        Moving onto the Basis Theorem,
        1. Remember that any two bases for a subspace share the same dimension or cardinality.
        2. Also, there can be multiple ways to define the basis of a subspace. 

        Continuing with the Invertible Matrix Theorem with Rank:

        Now let's dive into Section 3.1: Determinants Introduction.
        Key Definitions:
        1. Ai j submatrix is what you get after deleting the ith row and jth column of matrix A.
        2. For a 2x2 matrix A, determinant 'det A' is defined as 'ad - bc'.
        3. Cofactor expansion is used to solve determinants for square matrices that are sized 3x3 or larger.

        Note that:
        1. The signs in cofactor expansions depend on the position of the ai j element within the matrix.
        2. To find the determinant quickly, reduce the matrix to Row Echelon Form (REF).
        The result of row operations on determinants will be covered in 3.2.
        3. Multiply all the numbers on the main diagonal.

        For Section 3.2: Determinants Properties.
        Definitions:
        1. Column Operations have the same impact on determinants as row operations." "Remember that the determinant of A equals the determinant of its transpose, AT. Row operations on determinants perform as follow: row replacement has no effect, row swapping multiplies determinant by negative one, and row scaling multiplies the determinant by the scaling factor. An extended example of scaling is when a row is divided by 'k,' the determinant is multiplied by 1/k. 

        For invertible A (where each column is pivotal), the determinant of A is not zero. However, if A is non-invertible, the determinant is zero and, likely, one main diagonal entry of the REF is zero. 

        In the case of A being non-invertible, its rows and, if square, columns are linearly dependent. It is crucial to remember few math relations: det A equals det AT, det AB equals the product of det A and det B, and det A-1 equals 1 divided by det A. 

        Volume and Linear Transformation explains that a 'parallelepiped' is a multi-dimensional parallelogram (n > 2). For a 2x2 matrix A, the columns of A determine the area of the parallelogram, getting its absolute value as | det A |. Lastly, in a 3x3 matrix A,..." "The determinant of matrix A gives the area of the parallelepiped it forms. Regardless of swaps or replacements in rows/columns, the absolute determinant value remains unchanged. Within linear transformations on a parallelepiped, the area of T(S) equals the determinant of A, multiplied by the area of S, where T is the linear transformation determined by A, and S represents a parallelogram.

        Chapter 4.9 outlines Markov Chains applications. Key terms include the Probability vector, which sums to 1, and the Stochastic matrix, essentially a square matrix where columns are probability vectors. Also, the Markov Chain, which pairs a series of probability vectors with a stochastic matrix. A Steady State Vector signifies a probability, q, such that Pq equals q. All stochastic matrices have a steady state vector. A Regular Stochastic Matrix is a stochastic matrix whose some power ensures only strictly positive entities.

        To predict the next outcome in a Markov Chain, multiply P by xk to get xk+1." "Look for the steady state vector. Seek the basis of the null space using (P - I) q = 0 equation and ensure the sum of columns equals one. A steady state vector is essentially a probability vector. The initial state doesn't influence the Markov Chain's long-term behavior.

        Jumping to Section 5.1, Eigenvalues and Eigenvectors. An eigenvector of an n x n matrix A is a nonzero vector x adhering to Ax = λx for certain scalar λ. The Eigenvalue of A is a scalar λ with a nontrivial solution x of Ax = λx whereas Eigenspace incorporates zero vectors and all eigenvectors tied to λ. 

        To verify if a vector x is an eigenvector, multiply A*x and check if the product equals a scalar multiple of x. For discovering the eigenvector from an eigenvalue (7), solve (A - 7I)x = 0 and apply the parametric vector form. To find the eigenvalue λ, resolve (A - λI)x = 0 for a nontrivial solution and seek all solutions in the null space of (A - λI)." "Entries on the principal diagonal define 'x.' A matrix 'A' with '0' as an eigenvalue implies it's non-invertible. In that scenario, 'Ax' equals '0x,' and 'x' becomes a significant solution. Distinct eigenvalues correspond to independent eigenvectors, however, the converse isn't always true; independent eigenvectors can still share the same eigenvalue.

        Segment 5.2 presents 'The Characteristic Equation.' Here are the definitions:
        1. The Characteristic Polynomial is 'det(A - λI).'
        2. The Characteristic Equation is 'det(A - λI) equals zero.' 
        3. Trace refers to the sum of matrix diagonal entries. 
        4. Algebraic Multiplicity of an Eigenvalue indicates the count of eigenvalue roots in the characteristic polynomial. 
        5. Geometric Multiplicity of an Eigenvalue measures the dimension of Null '(A - λI)' for a specific eigenvalue λ. 

        To find eigenvalues, solve '(A - λI)x equals zero' for substantial solutions and identify all solutions to the null space of '(A - λI).' For an 'n x n' matrix 'A,' it's invertible solely when..." "Remember, A isn't an eigenvalue if the number 0 is excluded from eigenvalues and A's determinant is non-zero. When deriving a characteristic polynomial, implement the formula 'lambda squared minus lambda times trace, plus det A'. A simplified version of a 2nd degree characteristic polynomial. Beware that you cannot obtain the eigenvalues from a matrix's reduced form. Row operations alter eigenvalues.
        Take note of these key theorems:
        Theorem 4: Approach to Inverse a 2x2 Matrix
        Theorem 5: Alternative Formula to Determine Solution Set
        Theorem 6: Characteristics of Inversible Matrices
        Theorem 7: How to Inverse a Matrix
        Theorem 8: Laws Governing Invertible Matrices
        Theorem 9: Invertible and Linear Transformations
        Theorem 10: Expanding AB via Column-Row
        Theorem 11: Resolving Output Vector 'x'
        Theorem 12: Identifying Null Space of Matrix A
        Theorem 13: Assessing Matrix A's Column Space
        Theorem 14: Understanding the Rank Theorem
        Theorem 15: Comprehending the Basis Theorem

        Heading into Chapter 3, keep in mind:
        Theorem 1: Utilizing Cofactor Expansion for Determinants
        Theorem 2: Computing Shortcuts" "Today, we will delve into the world of determinants, starting with Theorem 3, where we will examine the impact of row operations. The intriguing IMT DLC will present itself in Theorem 4, followed by the exploration of Transpose Equivalence in Theorem 5. Theorem 6 will reveal the Multiplicative Property of Determinants. 

        Moving on, we will discover a new perspective of determinants as area and volume in Theorem 9, and we will see how these aspects are influenced by linear transformations in Theorem 10. 

        As we venture into Chapter 4, we will focus on Theorem 18's insight on the long-term behavior of a Markov Chain. 

        In Chapter 5, we get introduced to matrix problems, with Theorem 1 addressing the Eigenvalues of a Triangular Matrix. Rounding things off, Theorem 2 will enlighten us on Eigenvectors for Distinct Eigenvalues.

        In Section 5.3, we define a diagonal matrix as a matrix where non-zero entries exist only on the main diagonal, with all other entries being zeros. We introduce the concept of similar matrices, stating that a matrix A is similar to a matrix D if A equals PDP inverse, where P is an invertible matrix. Similar matrices share the same eigenvalues and determinant. However, while similar matrices must have the same characteristic polynomial, the converse is not true; matrices with the same eigenvalues may not be similar.

        Diagonalization refers to the process of expressing a matrix A as a product of a diagonal matrix D and an invertible matrix P. This technique is valuable for computing A raised to large powers. We differentiate between algebraic multiplicity, the number of times an eigenvalue appears, and geometric multiplicity, the number of linearly independent eigenvectors corresponding to an eigenvalue.

        The diagonalization formula A equals PDP inverse allows us to compute powers of A efficiently. According to Theorem 5, an n by n matrix A is diagonalizable if and only if it has n linearly independent eigenvectors, meaning that A's dimension equals the dimension of P. To diagonalize a matrix, we follow these steps: find eigenvalues by solving the determinant equation; find linearly independent eigenvectors by solving (A - λI)v = 0; construct P from these vectors; and construct D from the corresponding eigenvalues. Theorem 6 states that a matrix with n distinct eigenvalues is diagonalizable, while Theorem 7 addresses matrices with non-distinct eigenvalues, stating that the geometric multiplicity must be less than or equal to the algebraic multiplicity. For a matrix to be diagonalizable, the sum of the dimensions of the eigenspaces must equal the number of columns in the matrix.

        Section 5.5 introduces complex eigenvalues, where a complex number is defined as a + bi, with i being the imaginary unit. We define complex eigenvalues and eigenvectors, and the space of complex numbers. To find complex eigenvalues, we solve the characteristic polynomial. If it produces complex roots, these roots are the complex eigenvalues. The associated eigenvectors are determined by solving (A - λI)x = 0. The theorem highlights that for a real 2 by 2 matrix with complex eigenvalues, the matrix can be expressed in a specific form using the real and imaginary parts of the eigenvectors.

        In Section 10.2, we discuss Google PageRank, beginning with the definition of a stochastic matrix, characterized by columns that sum to one and always having at least one steady state. We also define a regular stochastic matrix, which guarantees a unique steady state. The concepts of dangling nodes and their effects on steady-state vectors are addressed, with the adjustment to replace dangling node columns with equal probabilities. The Google matrix formula is presented, which combines adjustments to create a matrix that models web page ranking.

        Section 6.1 focuses on the inner product, vector length, and orthogonality. We define the inner product of vectors, the length of a vector, and unit vectors. The distance between two vectors is established, and we define orthogonal vectors as those whose inner product equals zero. Orthogonal complements and subspaces in ℝn are discussed, emphasizing the closure under addition and scalar multiplication. Theorems illustrate the properties of the dot product, including symmetry, linearity, positivity, and the Pythagorean theorem for orthogonal vectors.

        Section 6.2 covers orthogonal sets, stating that an orthogonal set of nonzero vectors is linearly independent and forms a basis for the subspace they span. Orthogonal projections onto a line or plane are defined, alongside the properties of orthonormal sets and bases. Theorem 4 confirms that orthogonal sets are linearly independent, while Theorem 5 presents a method to find weights for linear combinations based on an orthogonal basis. The process of orthogonal projection is also detailed, including geometric representations and properties.

        Finally, Section 6.3 discusses orthogonal projections, highlighting that the projection of a vector onto a subspace provides the closest point in that subspace. The unique decomposition of vectors into orthogonal components is addressed, alongside theorems relating to orthogonal projections, approximation, and orthonormal bases. The relationship between orthogonal matrices and properties of matrices with orthonormal columns is also examined.

        This summary provides a comprehensive overview of the key concepts and theorems from the specified sections, serving as an effective lecture resource.
        '''
    maxDuration = 5  # minutes
    WPM = 160
    maxWords = int(maxDuration * WPM)
    
    response = convert_to_script(text)
    response = normalize_text(response)
    response = condense(response, maxWords)
    
    print("Final Response (length=" + str(len(response)))
    print(response)

    # Commented code is for testing

    # print("LENGTH BEFORE NORMALIZATION")
    # print(len(response))
    
    # response = normalize_text(response)
    # print("LENGTH AFTER NORMALIZATION")
    # print(len(response))
    # # print(response)
    
    # response = condense(response, maxWords)
    # print("LENGTH AFTER CONDENSING")
    # print(len(response))
    # print(response)
    