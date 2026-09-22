using System.IO.Compression;

namespace Navtool.App.DemoAnalysis;

// Deliberately unsafe, analysis-only conference fixture. Never invoke; remove before merge.
internal static class DemoOnlyZipSlipAnalysisFixture
{
    private static void ExtractForAnalysisOnly(ZipArchive archive, string outputDirectory)
    {
        foreach (var entry in archive.Entries)
        {
            var destination = Path.Combine(outputDirectory, entry.FullName);
            entry.ExtractToFile(destination);
        }
    }
}
