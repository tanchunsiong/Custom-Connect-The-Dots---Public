with
    
avgoutput as
(
Select
    measurename,
    unitofmeasure,
    'All SSH Login Failed Attempts' AS location,
    'All SSH Login Failed Attempts' AS organization,
    'ace60e7c-a6aa-4694-ba86-c3b66952558e' AS guid,
    'Average SSH Failed Login Attempt' as displayname,
    Max(timecreated) as timecreated,
    
    count(value) AS value
From
    DevicesInput TIMESTAMP BY timecreated
where
    measurename = 'SSH Failed Login Attempt'
Group by
    measurename, unitofmeasure,
    TumblingWindow(Second, 10)
    )


, alertoutput as (SELECT 
    'SSHSpike' AS alerttype, 
    'More than 10 Attacks per Second' AS message, 
    displayname,
    guid,
    measurename,
    unitofmeasure, 
    location,
    organization,
    MIN(timecreated) AS timecreated,
    count(value) AS tempMax,
    count(value) AS value
FROM 
    DevicesInput TIMESTAMP BY timecreated

GROUP BY 
    measurename, unitofmeasure,  displayname,
    guid,location,  organization,
    TumblingWindow(Second, 5)
 HAVING 
    tempMax > 10),avgoutput2 as
(
Select
    measurename,
    unitofmeasure,
    'All SSH Login Failed Attempts' AS location,
    'All SSH Login Failed Attempts' AS organization,
    'ace60e7c-a6aa-4694-ba86-c3b66952558e' AS guid,
    'Average SSH Reverse Mapping' as displayname,
    Max(timecreated) as timecreated,
    
    count(value) AS value
From
    DevicesInput TIMESTAMP BY timecreated
where
    measurename = 'SSH Reverse Mapping'
Group by
    measurename, unitofmeasure,
    TumblingWindow(Second, 10)
    )


,avgoutput3 as
(
Select
    measurename,
    unitofmeasure,
    'All SSH Attempts' AS location,
    'All SSH Attempts' AS organization,
    'ace60e7c-a6aa-4694-ba86-c3b66952558e' AS guid,
    'Average SSH Attempts' as displayname,
    Max(timecreated) as timecreated,
    
    count(value) AS value
From
    DevicesInput TIMESTAMP BY timecreated
where
    measurename = 'SSH Attempt'
Group by
    measurename, unitofmeasure,
    TumblingWindow(Second, 10)
    )



    
SELECT * INTO ehavgoutput FROM avgoutput
SELECT * INTO ehavgoutput2 FROM avgoutput2
SELECT * INTO ehavgoutput3 FROM avgoutput3
SELECT * INTO ehalertoutput FROM alertoutput

