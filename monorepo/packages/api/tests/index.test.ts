import { describe, it, expect } from "vitest";
import { getUser, createUser } from "../src/index";

describe("getUser", () => {
  it("returns a user for a valid ID", () => {
    const user = getUser(1);
    expect(user).toBeDefined();
    expect(user?.name).toBe("Alice");
  });

  it("returns undefined for a non-existent ID", () => {
    const user = getUser(999);
    expect(user).toBeUndefined();
  });
});
