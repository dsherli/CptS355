{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}

{-# HLINT ignore "Use foldr" #-}
module MathUtil where

import Debug.Trace
import Distribution.Simple.Utils (xargs)

add x y = x + y

sub x y = x - y

mul x y = x * y

divi x y = x `div` y

len1 [] = 0
len1 (x : xs) = 1 + len1 xs

len2 xs = if xs == [] then 0 else 1 + len2 (tail xs)

len3 xs
  | xs == [] = 0
  | otherwise = 1 + len3 (tail xs)

len4 xs = case xs of
  [] -> 0
  (_ : ys) -> 1 + len4 ys

inc1 = add 1

incrementList xs = map inc1 xs

squareList xs = map (\x -> x * x) xs

add1 x y = x + y

add2 = (\x y -> x + y)

even' x = x `mod` 2 == 0

evenOnly xs = filter even' xs

sumList xs = foldr add 0 xs

sumList' xs = foldl sub 0 xs

incrementList' xs = foldr (\x acc -> inc1 x : acc) [] xs

fac 0 = 1
fac n = n * fac (n - 1)

mul1 x y | trace ("mull1 called with: " ++ show x ++ " " ++ show y) False = undefined
mul1 x 1 = x
mul1 1 y = y
mul1 0 _ = 0
mul1 _ 0 = 0
mul1 x y = x + mul1 x (y - 1)

myFindIndexHelper (x : xs) n elm | trace ("x and n and elm: " ++ show x ++ ", " ++ show n ++ ", " ++ show elm) False = undefined
myFindIndexHelper [] n elm = -1
myFindIndexHelper (x : xs) n elm = if elm == x then n else myFindIndexHelper xs (n + 1) elm

myFindElement xs elm = myFindIndexHelper xs 0 elm

myFindElementHelper [] n cur = -1
myFindElementHelper (x : xs) n cur = if n == cur then x else myFindElementHelper xs n (cur + 1)

myFindIndex xs n = myFindElementHelper xs n 0

findMaxHelper [] max = max
findMaxHelper (x : xs) max
  | x > max = findMaxHelper xs x
  | otherwise = findMaxHelper xs max

findMax [] = -1
findMax (x : xs) = findMaxHelper xs x

myReverse [] = []
myReverse (x : xs) = myReverse xs ++ [x]

myTake _ [] = []
myTake 0 _ = []
myTake n (x : xs) = x : myTake (n - 1) xs

reverse' [] = []
reverse' (x : xs) = reverse' xs ++ [x]

take' _ [] = []
take' 0 _ = []
take' n (x : xs) = x : take' (n - 1) xs

splitByConditionHelper [] _ res = res
splitByConditionHelper (x : xs) c (leftList, rightList) =
  if c x
    then splitByConditionHelper xs c (leftList ++ [x], rightList)
    else splitByConditionHelper xs c (leftList, rightList ++ [x])

splitByCondition xs c = splitByConditionHelper xs c ([], [])