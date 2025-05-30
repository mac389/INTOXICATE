Function RoundToSpecifiedAge(age As Double) As Integer
    Dim specifiedAges As Variant
    specifiedAges = Array(20, 30, 40, 50, 60, 70) ' The target ages to round to
    
    Dim closestAge As Integer
    Dim minDifference As Double
    minDifference = 9999 ' Initialize with a large number
    
    Dim i As Integer
    For i = LBound(specifiedAges) To UBound(specifiedAges)
        Dim difference As Double
        difference = Abs(age - specifiedAges(i))
        If difference < minDifference Then
            minDifference = difference
            closestAge = specifiedAges(i)
        End If
    Next i
    
    RoundToSpecifiedAge = closestAge
End Function


Sub CalculateINTOXICATEScore_Shifted_AgeFixed()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("INTOXICATE")
    
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "C").End(xlUp).Row ' Adjusted from "A" to "C"
    
    Dim i As Long
    For i = 2 To lastRow
        Dim exposureCategory As String
        Dim age As Double, hr As Double, sbp As Double, gcs As Double
        Dim respiratoryInsufficiency As String, cirrhosis As String
        Dim dysrhythmia As String, secondICUReason As String
        
        ' Adjusted column references by adding 2 to each
        exposureCategory = ws.Cells(i, 3).Value
        age = ws.Cells(i, 4).Value
        age = RoundToSpecifiedAge(age)
        hr = ws.Cells(i, 5).Value
        sbp = ws.Cells(i, 6).Value
        gcs = ws.Cells(i, 7).Value
        respiratoryInsufficiency = ws.Cells(i, 8).Value
        cirrhosis = ws.Cells(i, 9).Value
        dysrhythmia = ws.Cells(i, 10).Value
        secondICUReason = ws.Cells(i, 11).Value


        ' Initialize scores
        Dim exposureScore As Integer, sbpScore As Integer, hrScore As Integer, gcsScore As Integer
        Dim respiratoryScore As Integer, cirrhosisScore As Integer, dysrhythmiaScore As Integer, secondaryDiagnosisScore As Integer
        
        ' Convert Exposure Category to a numerical score
  Select Case exposureCategory
            Case "Alcohol"
                exposureScore = -5
            Case "Analgesic"
                exposureScore = 1
            Case "Antidepressants"
                exposureScore = 0
            Case "Street Drugs"
                exposureScore = 1
            Case "Sedatives"
                exposureScore = -1
            Case "CO, As, CN"
                exposureScore = -6
            Case "Unknown "
                exposureScore = 2
            Case "Combination"
                exposureScore = 0
            Case Else
                exposureScore = 0 ' Default value if the category doesn't match
        End Select
        
       ' HR scoring
        If hr < 75 Then
            hrScore = 0
        ElseIf hr < 85 Then
            hrScore = 1
        ElseIf hr < 95 Then
            hrScore = 2
        ElseIf hr < 105 Then
            hrScore = 3
        Else
            hrScore = 4
        End If

        ' SBP scoring
        If sbp >= 140 Then
            sbpScore = -3
        ElseIf sbp >= 130 Then
            sbpScore = -1
        ElseIf sbp >= 120 Then
            sbpScore = 0
        ElseIf sbp >= 110 Then
            sbpScore = 1
        ElseIf sbp >= 100 Then
            sbpScore = 2
        Else
            sbpScore = 4
        End If
        
        ' GCS scoring
        If gcs >= 14 Then
            gcsScore = 0
        ElseIf gcs >= 9 Then
            gcsScore = 3
        ElseIf gcs >= 6 Then
            gcsScore = 7
        Else
            gcsScore = 9
        End If
        
        ' Binary conditions scoring
        respiratoryScore = IIf(respiratoryInsufficiency = "Yes", 8, 0)
        cirrhosisScore = IIf(cirrhosis = "Yes", 7, 0)
        dysrhythmiaScore = IIf(dysrhythmia = "Yes", 5, 0)
        secondaryDiagnosisScore = IIf(secondICUReason = "Yes", 7, 0)

        ' Calculate the endpoint including all scores; here age is corrected to reference values used for point system and the regression intercept was removed
        Dim endpoint As Double
        endpoint = exposureScore + ((age - 20) / 5) + hrScore + sbpScore + gcsScore + respiratoryScore + cirrhosisScore + dysrhythmiaScore + secondaryDiagnosisScore

        ws.Cells(i, 12).Value = endpoint ' Changed from column 10 to 12
    Next i
End Sub

