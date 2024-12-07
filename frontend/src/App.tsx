import AssignmentUploader from './components/AssignmentUploader';

function App() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">Auto Grader</h1>
      <AssignmentUploader />
    </div>
  );
}

export default App;