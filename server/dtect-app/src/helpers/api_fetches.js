export async function fetchauthlogs() {
    let response = await fetch('/authlogs')

    let logs = await response.json();

    if (logs.success) {
        return logs.logs;
    } else {
        return null;
    }
}