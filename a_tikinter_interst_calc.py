from tkinter import messagebox
from tkinter import *


def doCalc(*args):

    balance = float(loan_amt.get()) - float(deposit.get())
    annualInterestRate = float(interest_rate.get()) / 100.0
    #print balance
    monthlyInterest = float(annualInterestRate) / 12.0
    #print monthlyInterest
    
    found = False
    
    numMonths = int(repayment_time.get())
    if repayTimeChoice.get(ACTIVE) == "Years":
        numMonths *= 12
    
    lowerBound = balance / numMonths
    upperBound = (balance * (1 + monthlyInterest)**numMonths) / 12.0
    
    thisGuess = (lowerBound + upperBound) / 2
    
    lastLowGuess = lowerBound
    #print lowerBound
    lastHighGuess = upperBound
    #print upperBound
    #A counter to count number of itterations required to solve.
    i = 0
    if( numMonths <= 360):
        while not found:
            i += 1
            #print thisGuess
            
            thisBalance = balance
    
            #Itterate to find the final balance with current guess repayment amount.
            for month in range (1, numMonths + 1, 1):
                thisBalance -= thisGuess
                thisBalance = thisBalance + (monthlyInterest)*thisBalance
            
            if thisBalance < 0: #OverPayed 
                lastHighGuess = thisGuess
                thisGuess = (thisGuess + lastLowGuess) / 2
            elif thisBalance > 0: #UnderPayed
                lastLowGuess = thisGuess
                thisGuess = (thisGuess + lastHighGuess) / 2
            else:
                found = True
                
            if abs(thisBalance) < 0.001:
                found = True
        '''
        print "balance = ", balance
        print loan_amt.get()
        print "time = ", numMonths
        print repayment_time.get()
        print "interest = ", monthlyInterest
        print interest_rate.get()
        print "lowest payment = ", lowest_payment.get()
        '''
        totalInterest = numMonths * thisGuess - balance
        lowest_payment.set(thisGuess)
        total_interest.set(totalInterest)

def popUp(*args):
    doCalc(args)
    messagebox.showinfo("Answer!", lowest_payment.get())
    pass


top = Tk()

#Declaring Stringvars:
loan_amt = StringVar()
loan_amt.set(0)

deposit = StringVar()
deposit.set(0)

interest_rate = StringVar()
interest_rate.set(5.8)

repayment_time = StringVar()
repayment_time.set(120)

lowest_payment = StringVar()
lowest_payment.set("NA")

total_interest = StringVar()
total_interest.set("NA")

#Setting up the interface. Grid is in total 6x3

#Row1

#(1,1)Label one: Loan amount
Label(top, text="Loan amount ($): ").grid(row=1, column=1)
#(1,2)Slider for loan amount
loanAmtSlider = Scale(top, variable=loan_amt, from_=0, to=2000000, orient=HORIZONTAL, resolution=1000, length=200)
loanAmtSlider.grid(row=1, column=2)
#(1,3)Entry box for loan amount
loanEntry = Entry(textvariable=loan_amt, width=10)
loanEntry.grid(row=1, column=3)

#Row2
#(2,1)Label two: Deposit
Label(top, text="Deposit ($): ").grid(row=2, column=1)
#(2,2)Slider for Deposit amount
DepositAmtSlider = Scale(top, variable=deposit, from_=0, to=2000000, orient=HORIZONTAL, resolution=1000, length=200)
DepositAmtSlider.grid(row=2, column=2)
#(2,3)Entry box for Deposit amount
depositEntry = Entry(textvariable=deposit, width=10)
depositEntry.grid(row=2, column=3)

#Row3
#(3,1)Label three: Interest rate
Label(top, text="Interest Rate: ").grid(row=3, column=1)
#(3,2)Entry for interest rate
interestEntry = Entry(textvariable=interest_rate)
interestEntry.grid(row=3, column=2)
#(3,3)Label for interest
Label(top, text="Percent").grid(row=3, column=3)

#Row4
#(4,1)Label four: Repayment Time
Label(top, text="Repayment Time: ").grid(row=4, column=1)
#(4,2)Entry for repayment time
repaymentEntry = Entry(textvariable=repayment_time)
repaymentEntry.grid(row=4, column=2)
#(4,3)ListBox for months OR years
repayTimeChoice = Listbox(top, height=2)
repayTimeChoice.insert(1, "Months")
repayTimeChoice.insert(2, "Years")
repayTimeChoice.grid(row=4, column=3)
repayTimeChoice.activate(2)

#Row5
#(5,1)Label for Lowest payment
Label(top, text="Lowest payment ($):").grid(row=5, column=1)
#(5,2)Disply box for lowest payment
Label(top, textvariable=lowest_payment).grid(row=5, column=2)

#Row6
#(6,1)Label for Total interest
Label(top, text="Total Interest ($): ").grid(row=6, column=1)
#(6,2)Display box for total interest
Label(top, textvariable=total_interest).grid(row=6, column=2)

#Buttons
#Button to calculate value
calcButton = Button(top, text="Calculate", command=doCalc, fg="red")
calcButton.grid(row=5, column=3)

#Other button to show popup.
calcButtonPopup = Button(top, text="Calc+Popup", command=popUp, fg="blue")
calcButtonPopup.grid(row=6, column=3)

#Finishing touches.
for child in top.winfo_children():
    child.grid_configure(padx=5, pady=5)

#Dont end until user exits.
top.mainloop()
