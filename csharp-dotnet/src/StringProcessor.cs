using System.Globalization;
using System.Text.RegularExpressions;

namespace CSharpExample;

/// <summary>
/// String processing utilities with several untested edge cases.
/// </summary>
public static class StringProcessor
{
    /// <summary>
    /// Converts a string to title case (first letter of each word capitalized).
    /// Untested edge cases: null input, empty string, all-uppercase input,
    /// strings with extra whitespace, single-character words, hyphenated words.
    /// </summary>
    public static string ToTitleCase(string input)
    {
        if (input == null)
            throw new ArgumentNullException(nameof(input));

        if (string.IsNullOrWhiteSpace(input))
            return input;

        var textInfo = CultureInfo.InvariantCulture.TextInfo;
        return textInfo.ToTitleCase(input.ToLower());
    }

    /// <summary>
    /// Counts the number of words in a string, splitting on whitespace.
    /// Untested edge cases: null input, empty string, only whitespace,
    /// multiple consecutive spaces, tabs and newlines, leading/trailing spaces.
    /// </summary>
    public static int CountWords(string input)
    {
        if (input == null)
            throw new ArgumentNullException(nameof(input));

        var trimmed = input.Trim();
        if (trimmed.Length == 0)
            return 0;

        return Regex.Split(trimmed, @"\s+").Length;
    }

    /// <summary>
    /// Extracts all email addresses from a string.
    /// Untested: no tests at all. Edge cases: no emails, multiple emails,
    /// emails at start/end, malformed emails.
    /// </summary>
    public static List<string> ExtractEmails(string input)
    {
        if (input == null)
            throw new ArgumentNullException(nameof(input));

        var pattern = @"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}";
        var matches = Regex.Matches(input, pattern);
        var emails = new List<string>();

        foreach (Match match in matches)
        {
            emails.Add(match.Value);
        }

        return emails;
    }

    /// <summary>
    /// Truncates a string to the given max length, appending "..." if truncated.
    /// Untested: no tests at all. Edge cases: null input, max length less than 3,
    /// string exactly at max length, empty string.
    /// </summary>
    public static string Truncate(string input, int maxLength)
    {
        if (input == null)
            throw new ArgumentNullException(nameof(input));

        if (maxLength < 0)
            throw new ArgumentOutOfRangeException(nameof(maxLength));

        if (input.Length <= maxLength)
            return input;

        if (maxLength <= 3)
            return new string('.', maxLength);

        return input[..(maxLength - 3)] + "...";
    }
}
