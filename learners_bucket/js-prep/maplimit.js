Array.prototype.chop = function (size) {
  const temp = [...this];
  if (!size) return temp;

  const output = [];
  let i = 0;
  while (i < temp.length) {
    output.push(temp.slice(i, i + size));
    i = i + size;
  }
  return output;
};

const mapLimit = (arr, limit, fn) => {
  return new Promise((resolve, reject) => {
    const choppedArr = arr.chop(limit);

    const final = choppedArr.reduce((acc, cv) => {
      return acc.then((val) => {
        return new Promise((res, rej) => {
          const results = [];
          let tasksCompleted = 0;
          cv.forEach((e) => {
            fn(e, (error, value) => {
              if (error) {
                rej(error);
              } else {
                results.push(value);
                tasksCompleted++;
                if (tasksCompleted >= cv.length) {
                  res([...val, ...results]);
                }
              }
            });
          });
        });
      });
    }, Promise.resolve([]));
    final
      .then((result) => {
        resolve(result);
      })
      .catch((e) => {
        reject(e);
      });
  });
};

let numPromise = mapLimit([1, 2, 3, 4, 5], 3, function (num, callback) {
  setTimeout(function () {
    num = num * 2;
    console.log(num);
    // if (num == 6) {
    //   callback(true);
    // } else {
    //   callback(null, num);
    // }
    callback(null, num);
  }, 2000);
});

numPromise
  .then((result) => console.log("success:" + result))
  .catch((err) => console.log("no success", err));
