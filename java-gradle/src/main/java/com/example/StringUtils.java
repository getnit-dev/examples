package com.example;

/**
 * String utility functions. Entirely untested.
 */
public class StringUtils {

    /**
     * Reverses a string. Edge cases: null input, empty string,
     * single character, unicode/emoji characters.
     */
    public static String reverse(String s) {
        if (s == null) {
            return null;
        }
        return new StringBuilder(s).reverse().toString();
    }

    /**
     * Checks whether a string is a palindrome (case-insensitive).
     * Edge cases: null input, empty string, single character,
     * strings with spaces, mixed case.
     */
    public static boolean isPalindrome(String s) {
        if (s == null) {
            return false;
        }
        String cleaned = s.replaceAll("\\s+", "").toLowerCase();
        String reversed = new StringBuilder(cleaned).reverse().toString();
        return cleaned.equals(reversed);
    }

    /**
     * Counts words in a string, splitting on whitespace.
     * Edge cases: null input, empty string, multiple spaces,
     * leading/trailing whitespace, only whitespace.
     */
    public static int countWords(String s) {
        if (s == null || s.trim().isEmpty()) {
            return 0;
        }
        return s.trim().split("\\s+").length;
    }
}
