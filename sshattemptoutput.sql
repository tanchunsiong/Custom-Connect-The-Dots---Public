with
    
    indFailedAttemptOutput as (

Select
   *
From
    DevicesInput TIMESTAMP BY timecreated
where
    measurename = 'SSH Failed Login Attempt' and ip is not null

    ),
    
    indReverseMappingOutput as (

Select
   *
From
    DevicesInput TIMESTAMP BY timecreated
where
    measurename = 'SSH Reverse Mapping' and ip is not null

    )
    ,
    
    indAttemptOutput as (

Select
   *
From
    DevicesInput TIMESTAMP BY timecreated
where
    measurename = 'SSH Attempt' and ip is not null

    )
    


SELECT * INTO storageoutput FROM indFailedAttemptOutput
SELECT * INTO storagermoutput FROM indReverseMappingOutput
SELECT * INTO storageAttemptoutput FROM indAttemptOutput