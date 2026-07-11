const styles = {
  pending:    "bg-yellow-500/20 text-yellow-400",
  processing: "bg-blue-500/20 text-blue-400",
  completed:  "bg-green-500/20 text-green-400",
  failed:     "bg-red-500/20 text-red-400",
};

export default function StatusBadge({ status }) {
  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${styles[status] ?? styles.pending}`}>
      {status}
    </span>
  );
}
