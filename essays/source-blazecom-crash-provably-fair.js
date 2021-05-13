import React from "react";
import ReactDOM from "react-dom";
import crypto from "crypto";

import "./styles.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      server_seed: "",
      amount: 10
    };
  }
  render() {
    // an example with 10 seeds

    const chain = [this.state.server_seed];

    for (let i = 0; i < this.state.amount; i++) {
      chain.push(
        crypto
          .createHash("sha256")
          .update(chain[chain.length - 1])
          .digest("hex")
      );
    }

    // the hash of bitcoin block 570128 (https://medium.com/@blazedev/blaze-com-crash-seeding-event-v2-d774d7aeeaad)
    const clientSeed =
      "0000000000000000000415ebb64b0d51ccee0bb55826e43846e5bea777d91966";

    return (
      <div className="App">
        <h3>Enter the server seed of your game</h3>
        <input
          value={this.state.server_seed}
          onChange={e => this.setState({ server_seed: e.target.value })}
        />
        <br />
        <br />
        <h3>Enter the # of games to view before this one</h3>
        <input
          value={this.state.amount}
          onChange={e => this.setState({ amount: e.target.value })}
        />

        <hr />
        <h1>Crash points:</h1>

        {!this.state.server_seed || this.state.server_seed.length !== 64 ? (
          <h3 style={{ color: "red" }}>
            Please enter a server seed to view this table
          </h3>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Crash point</th>
                <th>Seed</th>
                <th>Hash (hmac with client seed)</th>
              </tr>
            </thead>
            <tbody>
              {chain.map((seed, index) => {
                const hash = crypto
                  .createHmac("sha256", seed)
                  .update(clientSeed)
                  .digest("hex");

                const divisible = (hash, mod) => {
                  let val = 0;

                  let o = hash.length % 4;
                  for (let i = o > 0 ? o - 4 : 0; i < hash.length; i += 4) {
                    val =
                      ((val << 16) + parseInt(hash.substring(i, i + 4), 16)) %
                      mod;
                  }

                  return val === 0;
                };

                function getPoint(hash) {
                  // In 1 of 15 games the game crashes instantly.
                  if (divisible(hash, 15)) return 0;

                  // Use the most significant 52-bit from the hash to calculate the crash point
                  let h = parseInt(hash.slice(0, 52 / 4), 16);
                  let e = Math.pow(2, 52);

                  const point = (
                    Math.floor((100 * e - h) / (e - h)) / 100
                  ).toFixed(2);

                  return point;
                }

                const point = getPoint(hash);
                return (
                  <tr>
                    <td style={{ color: point < 2 ? "red" : "green" }}>
                      {point}
                    </td>
                    <td>{seed}</td>
                    <td>{hash}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    );
  }
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
