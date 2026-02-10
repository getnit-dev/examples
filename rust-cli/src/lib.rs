use std::collections::HashMap;

/// Validates whether a string looks like a valid email address.
/// Untested edge cases: empty string, multiple @ signs, consecutive dots,
/// unicode characters, very long local parts.
pub fn validate_email(email: &str) -> bool {
    if email.is_empty() {
        return false;
    }

    let parts: Vec<&str> = email.splitn(2, '@').collect();
    if parts.len() != 2 {
        return false;
    }

    let local = parts[0];
    let domain = parts[1];

    if local.is_empty() || domain.is_empty() {
        return false;
    }

    if local.len() > 64 {
        return false;
    }

    if !domain.contains('.') {
        return false;
    }

    let domain_parts: Vec<&str> = domain.split('.').collect();
    if domain_parts.iter().any(|p| p.is_empty()) {
        return false;
    }

    let tld = domain_parts.last().unwrap();
    if tld.len() < 2 {
        return false;
    }

    true
}

/// Parses a simple KEY=VALUE config format into a HashMap.
/// Untested edge cases: empty input, lines with no '=', duplicate keys,
/// values containing '=', whitespace-only lines, comment lines.
pub fn parse_config(input: &str) -> Result<HashMap<String, String>, String> {
    let mut config = HashMap::new();

    for (line_num, line) in input.lines().enumerate() {
        let trimmed = line.trim();

        if trimmed.is_empty() || trimmed.starts_with('#') {
            continue;
        }

        let eq_pos = trimmed
            .find('=')
            .ok_or_else(|| format!("line {}: missing '=' delimiter", line_num + 1))?;

        let key = trimmed[..eq_pos].trim().to_string();
        let value = trimmed[eq_pos + 1..].trim().to_string();

        if key.is_empty() {
            return Err(format!("line {}: empty key", line_num + 1));
        }

        config.insert(key, value);
    }

    Ok(config)
}

/// Truncates a string to the given max length, appending "..." if truncated.
/// Untested: no tests at all.
pub fn truncate(s: &str, max_len: usize) -> String {
    if s.len() <= max_len {
        return s.to_string();
    }
    if max_len <= 3 {
        return ".".repeat(max_len);
    }
    format!("{}...", &s[..max_len - 3])
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_email_basic() {
        assert!(validate_email("user@example.com"));
        assert!(!validate_email("not-an-email"));
    }

    #[test]
    fn test_parse_config_basic() {
        let input = "host=localhost\nport=8080";
        let config = parse_config(input).unwrap();
        assert_eq!(config.get("host").unwrap(), "localhost");
        assert_eq!(config.get("port").unwrap(), "8080");
    }
}
