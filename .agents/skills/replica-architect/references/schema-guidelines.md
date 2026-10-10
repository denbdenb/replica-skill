# Schema Guidelines and Platform Guidance

Reference material for `replica-architect`. Load this reference only when designing
the persistent data model and authoring migrations for your selected platform.

## 1. Web Database Schema (Postgres / SQL)

For Web SaaS applications using Postgres (Supabase, Neon) or SQLite (Turso):

```sql
create table bookings (
  id uuid primary key default gen_random_uuid(),
  event_type_id uuid not null references event_types(id) on delete cascade,
  host_id uuid not null references users(id) on delete cascade,
  start_at timestamptz not null,
  end_at timestamptz not null,
  guest_name text not null,
  guest_email text not null,
  guest_timezone text not null,
  status text not null default 'confirmed'
    check (status in ('confirmed', 'cancelled', 'rescheduled')),
  answers jsonb not null default '{}',
  created_at timestamptz not null default now(),
  constraint no_zero_length check (end_at > start_at)
);
create index on bookings (host_id, start_at);
```

### Access and Row Level Security (RLS)
- On Supabase / Postgres: enable RLS and write one explicit policy per operation (select, insert, update, delete).
- In application data layers: verify `user_id` ownership on every query.

## 2. Desktop Database Schema (WinUI 3 / WPF / SQLite)

For native desktop applications:
- Use local SQLite via Microsoft.Data.Sqlite or Entity Framework Core.
- Store connection string in local user app data folder (`AppData\Local\<App>`).
- Enforce foreign keys with `PRAGMA foreign_keys = ON;`.
- Use transactions for multi-record operations.

## 3. Mobile Database Schema (Android Room / iOS CoreData)

For mobile applications:
- Android: Define `@Entity`, `@PrimaryKey`, and `@ForeignKey(onDelete = CASCADE)`.
- Use Room TypeConverters for timestamps (store epoch millis or ISO strings in UTC).
- Enforce unique indices with `@Index(value = ["slot_time"], unique = true)`.
