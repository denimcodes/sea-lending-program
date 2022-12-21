from seahorse.prelude import *

declare_id("2ZR1496ffaC7zFLLEUMrpy5LyMDJzMv99fp6mK4hb5sG")


class LendingMarket(Account):
    owner: Pubkey
    bump: u8


class Reserve(Account):
    lending_market: Pubkey
    liquidity_mint: Pubkey
    liquidity_supply: Pubkey
    liquidity_available_amount: u64
    borrowed_amount: u64
    collateral_mint: Pubkey
    collateral_supply: Pubkey
    collateral_total_amount: u64


class Obligation(Account):
    owner: Pubkey
    lending_market: Pubkey
    reserve: Pubkey
    deposited_amount: u64
    borrowed_amount: u64


@instruction
def init_lending_market(owner: Signer, lending_market: Empty[LendingMarket]):
    bump = lending_market.bump()
    lending_market = lending_market.init(payer=owner, seeds=["lending-market", owner])
    lending_market.owner = owner.key()
    lending_market.bump = bump


@instruction
def init_reserve(
    signer: Signer,
    reserve: Empty[Reserve],
    lending_market: LendingMarket,
    liquidity_mint: TokenMint,
    liquidity_supply: Empty[TokenAccount],
    collateral_mint: Empty[TokenMint],
    collateral_supply: Empty[TokenAccount],
):
    reserve = reserve.init(payer=signer, seeds=["reserve"])
    liquidity_supply = liquidity_supply.init(
        payer=signer,
        seeds=["liquidity-supply", liquidity_mint],
        mint=liquidity_mint,
        authority=lending_market,
    )
    collateral_mint = collateral_mint.init(
        payer=signer, seeds=["collateral-mint"], decimals=6, authority=lending_market
    )
    collateral_supply = collateral_supply.init(
        payer=signer,
        seeds=["collateral-supply", collateral_mint],
        mint=collateral_mint,
        authority=lending_market,
    )

    reserve.lending_market = lending_market.key()
    reserve.liquidity_mint = liquidity_mint.key()
    reserve.liquidity_supply = liquidity_supply.key()
    reserve.collateral_mint = collateral_mint.key()
    reserve.collateral_supply = collateral_supply.key()

    reserve.liquidity_available_amount = 0
    reserve.borrowed_amount = 0
    reserve.collateral_total_amount = 0


@instruction
def init_obligation(
    owner: Signer,
    obligation: Empty[Obligation],
    lending_market: LendingMarket,
    reserve: Reserve,
):
    obligation = obligation.init(payer=owner, seeds=["obligation", owner])
    obligation.lending_market = lending_market.key()
    obligation.reserve = reserve.key()
    obligation.deposited_amount = 0
    obligation.borrowed_amount = 0


@instruction
def supply(
    owner: Signer,
    lending_market: LendingMarket,
    reserve: Reserve,
    obligation: Obligation,
    liquidity_mint: TokenMint,
    owner_liquidity_supply: TokenAccount,
    reserve_liquidity_supply: TokenAccount,
    reserve_collateral_mint: TokenMint,
    reserve_collateral_supply: TokenAccount,
    liquidity_amount: u64,
):
    assert owner.key() == obligation.owner, "Signer is not owner of obligation"
    assert (
        lending_market.key() == obligation.lending_market
        and reserve.key() == obligation.reserve
    ), "Lending market or reserve is not matched for obligation"

    reserve.liquidity_available_amount += liquidity_amount
    reserve.collateral_total_amount += liquidity_amount
    obligation.deposited_amount += liquidity_amount

    owner_liquidity_supply.transfer(
        to=reserve_liquidity_supply, authority=owner, amount=liquidity_amount
    )
    bump = lending_market.bump
    reserve_collateral_mint.mint(
        to=reserve_collateral_supply,
        authority=lending_market,
        amount=liquidity_amount,
        signer=["lending-market", owner, bump],
    )


@instruction
def borrow(
    owner: Signer,
    lending_market: LendingMarket,
    reserve: Reserve,
    obligation: Obligation,
    owner_liquidity_supply: TokenAccount,
    reserve_liquidity_supply: TokenAccount,
    borrow_amount: u64,
):
    assert owner.key() == obligation.owner, "Signer is not owner of obligation"
    assert (
        lending_market.key() == obligation.lending_market
        and reserve.key() == obligation.reserve
    ), "Lending market or reserve is not matched for obligation"
    assert (
        borrow_amount < obligation.deposited_amount
    ), "Borrowed amount cannot be more than deposited amount"

    reserve.borrowed_amount += borrow_amount
    reserve.liquidity_available_amount -= borrow_amount
    obligation.borrowed_amount += borrow_amount

    bump = lending_market.bump
    reserve_liquidity_supply.transfer(
        to=owner_liquidity_supply,
        amount=borrow_amount,
        authority=lending_market,
        signer=["lending-market", owner, bump],
    )


@instruction
def withdraw(
    owner: Signer,
    lending_market: LendingMarket,
    reserve: Reserve,
    obligation: Obligation,
    liquidity_mint: TokenMint,
    owner_liquidity_supply: TokenAccount,
    reserve_liquidity_supply: TokenAccount,
    reserve_collateral_mint: TokenMint,
    reserve_collateral_supply: TokenAccount,
    withdraw_amount: u64,
):
    assert owner.key() == obligation.owner, "Signer is not owner of obligation"
    assert (
        lending_market.key() == obligation.lending_market
        and reserve.key() == obligation.reserve
    ), "Lending market or reserve is not matched for obligation"
    assert obligation.borrowed_amount == 0, "Outstanding borrowed amount is not repaid"
    assert (
        withdraw_amount <= obligation.deposited_amount
    ), "Withdraw amount cannot be more than deposited amount"

    reserve.liquidity_available_amount -= withdraw_amount
    reserve.collateral_total_amount -= withdraw_amount
    obligation.deposited_amount -= withdraw_amount

    bump = lending_market.bump
    reserve_liquidity_supply.transfer(
        to=owner_liquidity_supply,
        authority=lending_market,
        amount=withdraw_amount,
        signer=["lending-market", owner, bump],
    )
    reserve_collateral_mint.burn(
        holder=reserve_collateral_supply,
        authority=lending_market,
        amount=withdraw_amount,
        signer=["lending-market", owner, bump],
    )


@instruction
def repay(
    owner: Signer,
    lending_market: LendingMarket,
    reserve: Reserve,
    obligation: Obligation,
    owner_liquidity_supply: TokenAccount,
    reserve_liquidity_supply: TokenAccount,
    repay_amount: u64,
):
    assert owner.key() == obligation.owner, "Signer is not owner of obligation"
    assert (
        lending_market.key() == obligation.lending_market
        and reserve.key() == obligation.reserve
    ), "Lending market or reserve is not matched for obligation"
    assert (
        repay_amount <= obligation.borrowed_amount
    ), "Repaid amount cannot be greater than borrowed amount"

    reserve.borrowed_amount -= repay_amount
    reserve.liquidity_available_amount += repay_amount
    obligation.borrowed_amount -= repay_amount

    owner_liquidity_supply.transfer(
        to=reserve_liquidity_supply, amount=repay_amount, authority=owner
    )
