### Seahorse Lending Program

A simple example of a Solana smart contract written with Seahorse framework in Python language. It is a lending and borrowing program. Users can lend, borrow, repay and withdraw tokens.

#### Get started

The program is written with [Solana playground](https://beta.solpg.io). It is a beginner friendly web code editor built for writing, building, deploying and testing Solana smart contracts.

I recommend to follow this [tutorial](https://beta.solpg.io/tutorials/hello-seahorse) to get an understanding of the playground and Seahorse framework.

Now let's get started with writing the program in the playground. For now we will simply take the code from the repo to the playground.

1. Open the [playground](https://beta.solpg.io) in browser .
2. Delete the current python file. Create a new file and name it `sea_lending_program.py`. Copy the contents of the file with the same name from the repo and pase it here.
3. Now click on Build & Deploy tab on the toolbar on the left. Click on build button. The status of the build will be shown on the console.
4. Deploy the program.

#### Program state

Solana program states are stored in data accounts. There are three accounts involved here which are used for storing the state of the lending program.

1. `LendingProgram` -> This account stores the owner which has authority to manage tokens of reserve.
2. `Reserve` -> The reserve holds tokens of specific mint which are deposited by the users. It has state which keeps tracks of liquidity tokens and collateral tokens of users.
3. `Obligation` -> This account is a contract between user and the lending program. It keeps track of users deposits and borrows from reserve.

#### Program Instructions

Instructions are functions where logic of the program is stored. We can create new accounts, create tokens, mint and transfer tokens with instructions. Instructions can be called from client programs.

There are seven instructions in this program.

1. `init_lending_market` -> Create new lending market account.
2. `init_reserve` -> Create new reserve account. Also create liquidity and collateral token accounts.
3. `init_obligation` -> Create new obligation for user.
4. `supply` -> Users can lend tokens by calling this instruction with token mint and token account.
5. `borrow` -> Borrow tokens from the reserve
6. `repay` -> Repay borrowed tokens
7. `withdraw` -> Withdraw all the deposited tokens.

#### Test

1. Copy the contents from `seahorse.test.ts` to the file with same name in Solana playground.
2. Click on Test button.
3. The test results will be shown on console.

#### Todo

- [ ] Setup borrow and supply rates.
- [ ] Get market data from oracle (pyth).

#### Motivation

The program written is inspired from Solana Program Library Lending Program.
