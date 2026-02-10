using CSharpExample;
using Xunit;

namespace CSharpExample.Tests;

public class StringProcessorTests
{
    [Fact]
    public void ToTitleCase_BasicInput_ReturnsCorrectResult()
    {
        var result = StringProcessor.ToTitleCase("hello world");
        Assert.Equal("Hello World", result);
    }

    [Fact]
    public void CountWords_BasicSentence_ReturnsCorrectCount()
    {
        var result = StringProcessor.CountWords("the quick brown fox");
        Assert.Equal(4, result);
    }
}
