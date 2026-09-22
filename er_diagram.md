# ER Diagram

```mermaid
erDiagram
    USERS {
        int user_id PK
        varchar username UK
        varchar password
        varchar role
    }

    BOOKS {
        int book_id PK
        varchar isbn
        varchar title
        varchar author
        varchar category
        int copies_available
        date created_date
    }

    MEMBERS {
        int member_id PK
        varchar name
        varchar email
        varchar member_type
        varchar status
    }

    ISSUE_TRANSACTIONS {
        int transaction_id PK
        int book_id FK
        int member_id FK
        date issue_date
        date return_date
    }

    BOOKS ||--o{ ISSUE_TRANSACTIONS : "is issued in"
    MEMBERS ||--o{ ISSUE_TRANSACTIONS : "borrows"
```

Note: the diagram shows the logical relationships expected by the application. If your existing MySQL schema does not declare foreign-key constraints, the relationships are still enforced by the application queries but are not database-level FK constraints.
