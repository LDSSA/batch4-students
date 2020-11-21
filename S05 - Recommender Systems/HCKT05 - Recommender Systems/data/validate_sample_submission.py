def validate_submission(y_pred_file):
    """
    Validate that y_pred file is a valid prediction file.
    
    Args:
        y_pred_file: Predicted values object in sample_submission format
    Returns:
        bool: Validation succeeded, if false a detailed error message will be
              supplied
    Raises:
        Any exception will be caught and str(exc) presented to the students
    """
        
    if len(y_pred_file.columns) != 2:
        raise ValueError(f"Make sure you have only two columns in your dataset with\
        names User-ID and ISBN!")
    
    if all(y_pred_file.columns == ['User-ID','ISBN']) != True:
        raise ValueError(f"Make sure you have only two columns in your dataset with\
        names User-ID and ISBN!") 

    if y_pred_file.groupby('User-ID').count().ISBN.unique()[0] != 10:
        raise ValueError(f"You have to submit 10 (and only 10) books per user!")
        
    if len(y_pred_file.groupby('User-ID').count().ISBN.unique()) != 1:
        raise ValueError(f"You have to submit 10 (and only 10) books per user!")

    if len(y_pred_file['User-ID'].unique()) != 589:
        raise ValueError(f"Make sure you have all test users in your submission!")
    
    return True