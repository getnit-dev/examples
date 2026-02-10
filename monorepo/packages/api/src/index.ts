export interface User {
  id: number;
  name: string;
  email: string;
}

const users: Map<number, User> = new Map([
  [1, { id: 1, name: "Alice", email: "alice@example.com" }],
  [2, { id: 2, name: "Bob", email: "bob@example.com" }],
]);

/**
 * Retrieves a user by ID.
 * Untested edge cases: negative ID, non-integer ID, ID = 0.
 */
export function getUser(id: number): User | undefined {
  if (!Number.isInteger(id) || id <= 0) {
    return undefined;
  }
  return users.get(id);
}

/**
 * Creates a new user, returning the assigned ID.
 * Untested edge cases: empty name, empty email, duplicate email,
 * whitespace-only name.
 */
export function createUser(name: string, email: string): User {
  const trimmedName = name.trim();
  const trimmedEmail = email.trim().toLowerCase();

  if (!trimmedName) {
    throw new Error("Name is required");
  }
  if (!trimmedEmail) {
    throw new Error("Email is required");
  }

  for (const user of users.values()) {
    if (user.email === trimmedEmail) {
      throw new Error(`Email already exists: ${trimmedEmail}`);
    }
  }

  const id = users.size + 1;
  const user: User = { id, name: trimmedName, email: trimmedEmail };
  users.set(id, user);
  return user;
}

/**
 * Searches users by partial name match (case-insensitive).
 * Untested: no tests at all. Edge cases: empty query, special regex chars,
 * no matches, all matches.
 */
export function searchUsers(query: string): User[] {
  const lower = query.toLowerCase();
  const results: User[] = [];
  for (const user of users.values()) {
    if (user.name.toLowerCase().includes(lower)) {
      results.push(user);
    }
  }
  return results;
}
