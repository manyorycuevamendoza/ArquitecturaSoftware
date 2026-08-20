export class InMemoryLeaseApplicationRepository {
  #applications = new Map();
  #idempotencyKeys = new Map();

  find(id) { return this.#applications.get(id) ?? null; }
  findByIdempotencyKey(key) { const id = this.#idempotencyKeys.get(key); return id ? this.find(id) : null; }
  add(application) {
    if (this.#idempotencyKeys.has(application.idempotencyKey)) throw new Error("Idempotency key already exists.");
    this.#idempotencyKeys.set(application.idempotencyKey, application.id);
    this.#applications.set(application.id, application);
  }
  save(application) { this.#applications.set(application.id, application); }
}
