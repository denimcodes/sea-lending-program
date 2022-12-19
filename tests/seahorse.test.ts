// No imports needed: web3, anchor, pg and more are globally available

describe("sea lending program", async () => {
  const owner = pg.wallet;
  const connection = pg.connection;

  const programIdPk = new web3.PublicKey(pg.PROGRAM_ID);

  let lendingMarketPk: web3.PublicKey;
  let reservePk: web3.PublicKey;
  let obligationPk: web3.PublicKey;

  let liquidityMintPk = new web3.PublicKey(
    "B6juGJRuJKt3tiqzdefNYxrTUoygvzBiZLrYa6vxPicy"
  );
  let ownerLiquiditySupplyPk = new web3.PublicKey(
    "DCNUNofZVPEAeXCmVo1UBt65SCPFwRcaySuJghmgKyYs"
  );
  let reserveLiquiditySupplyPk: web3.PublicKey;

  let collateralMintPk: web3.PublicKey;
  let reserveCollateralSupplyPk: web3.PublicKey;

  before(async () => {
    [lendingMarketPk] = web3.PublicKey.findProgramAddressSync(
      [Buffer.from("lending-market"), owner.publicKey.toBuffer()],
      programIdPk
    );
    [reservePk] = web3.PublicKey.findProgramAddressSync(
      [Buffer.from("reserve")],
      programIdPk
    );
    [obligationPk] = web3.PublicKey.findProgramAddressSync(
      [Buffer.from("obligation"), owner.publicKey.toBuffer()],
      programIdPk
    );
    [reserveLiquiditySupplyPk] = web3.PublicKey.findProgramAddressSync(
      [Buffer.from("liquidity-supply"), liquidityMintPk.toBuffer()],
      programIdPk
    );
    [collateralMintPk] = web3.PublicKey.findProgramAddressSync(
      [Buffer.from("collateral-mint")],
      programIdPk
    );
    [reserveCollateralSupplyPk] = web3.PublicKey.findProgramAddressSync(
      [Buffer.from("collateral-supply"), collateralMintPk.toBuffer()],
      programIdPk
    );
  });

  it("init lending market", async () => {
    const accountInfo = await pg.program.account.lendingMarket.getAccountInfo(
      lendingMarketPk
    );
    if (!accountInfo) {
      let txSign = await pg.program.methods
        .initLendingMarket()
        .accounts({
          owner: owner.publicKey,
          lendingMarket: lendingMarketPk,
        })
        .rpc();

      console.log(`https://explorer.solana.com/tx/${txSign}?cluster=devnet`);
    }
  });

  it("init reserve", async () => {
    const accountInfo = await pg.program.account.lendingMarket.getAccountInfo(
      reservePk
    );
    if (!accountInfo) {
      let txSign = await pg.program.methods
        .initReserve()
        .accounts({
          signer: owner.publicKey,
          reserve: reservePk,
          lendingMarket: lendingMarketPk,
          liquidityMint: liquidityMintPk,
          liquiditySupply: reserveLiquiditySupplyPk,
          collateralMint: collateralMintPk,
          collateralSupply: reserveCollateralSupplyPk,
        })
        .rpc();

      console.log(`https://explorer.solana.com/tx/${txSign}?cluster=devnet`);
    }
  });

  it("init obligation", async () => {
    const accountInfo = await pg.program.account.lendingMarket.getAccountInfo(
      reservePk
    );
    if (!accountInfo) {
      let txSign = await pg.program.methods
        .initObligation()
        .accounts({
          owner: owner.publicKey,
          obligation: obligationPk,
          reserve: reservePk,
          lendingMarket: lendingMarketPk,
        })
        .rpc();

      console.log(`https://explorer.solana.com/tx/${txSign}?cluster=devnet`);
    }
  });

  it("supply tokens", async () => {
    let txSign = await pg.program.methods
      .supply(new anchor.BN(200_000_000)) // 200 tokens
      .accounts({
        owner: owner.publicKey,
        lendingMarket: lendingMarketPk,
        reserve: reservePk,
        obligation: obligationPk,
        liquidityMint: liquidityMintPk,
        ownerLiquiditySupply: ownerLiquiditySupplyPk,
        reserveLiquiditySupply: reserveLiquiditySupplyPk,
        reserveCollateralMint: collateralMintPk,
        reserveCollateralSupply: reserveCollateralSupplyPk,
      })
      .rpc();

    console.log(`https://explorer.solana.com/tx/${txSign}?cluster=devnet`);
  });

  it("borrow tokens", async () => {
    let txSign = await pg.program.methods
      .borrow(new anchor.BN(100_000_000)) // 100 tokens
      .accounts({
        owner: owner.publicKey,
        lendingMarket: lendingMarketPk,
        reserve: reservePk,
        obligation: obligationPk,
        ownerLiquiditySupply: ownerLiquiditySupplyPk,
        reserveLiquiditySupply: reserveLiquiditySupplyPk,
      })
      .rpc();

    console.log(`https://explorer.solana.com/tx/${txSign}?cluster=devnet`);
  });

  it("repay tokens", async () => {
    let txSign = await pg.program.methods
      .repay(new anchor.BN(100_000_000)) // 100 tokens
      .accounts({
        owner: owner.publicKey,
        lendingMarket: lendingMarketPk,
        reserve: reservePk,
        obligation: obligationPk,
        ownerLiquiditySupply: ownerLiquiditySupplyPk,
        reserveLiquiditySupply: reserveLiquiditySupplyPk,
      })
      .rpc();

    console.log(`https://explorer.solana.com/tx/${txSign}?cluster=devnet`);
  });

  it("withdraw tokens", async () => {
    let txSign = await pg.program.methods
      .withdraw(new anchor.BN(200_000_000)) // 200 tokens
      .accounts({
        owner: owner.publicKey,
        lendingMarket: lendingMarketPk,
        reserve: reservePk,
        obligation: obligationPk,
        liquidityMint: liquidityMintPk,
        ownerLiquiditySupply: ownerLiquiditySupplyPk,
        reserveLiquiditySupply: reserveLiquiditySupplyPk,
        reserveCollateralMint: collateralMintPk,
        reserveCollateralSupply: reserveCollateralSupplyPk,
      })
      .rpc();

    console.log(`https://explorer.solana.com/tx/${txSign}?cluster=devnet`);
  });
});
