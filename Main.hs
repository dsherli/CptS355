import MathUtil

main = do
  putStrLn "Enter num1: "
  num1String <- getLine
  putStrLn "Enter num2: "
  num2String <- getLine
  let num1 = read num1String :: Int
  let num2 = read num2String :: Int
  let res = add num1 num2
  putStrLn ("Sum = " ++ show res)