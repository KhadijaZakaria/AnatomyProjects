using UnityEngine;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{
    public PuzzlePieceRandomizer randomizer; // Assign this in the Inspector

    public GameObject startButton; // Assign the Start button in the Inspector
    public GameObject[] puzzlePieces; // Assign all puzzle pieces in the Inspector
    public Text timerText; // Assign the Timer Text UI element in the Inspector
    public Text gameMessageText; // Reference to the message UI element
    public GameObject restartButton; // Assign the Restart button in the Inspector

    private float timer = 0f;
    private float maxTime = 421f; // 7 minutes in seconds
    private bool gameStarted = false;

    public static bool isGameActive = true; // Static field to track game state

    void Start()
    {
        // Ensure puzzle pieces are inactive initially
        foreach (GameObject piece in puzzlePieces)
        {
            piece.SetActive(false);
        }

        // Hide the restart button initially
        restartButton.SetActive(false);

        // Hide the message text
        gameMessageText.text = "";
        gameMessageText.gameObject.SetActive(false);

        timerText.text = "Time: 07:00"; // Initial timer display
    }

    void Update()
    {
        if (gameStarted)
        {
            // Update the timer
            if (timer < maxTime - 1)
            {
                timer += Time.deltaTime;
                UpdateTimerUI();
            }
            else
            {
                // Stop the game if time runs out
                TimerEnded(false);
            }

            // Check if all pieces are snapped into place
            if (AllPiecesSnapped())
            {
                TimerEnded(true);
            }
        }
    }

    public void StartGame()
    {
        // Hide the start button
        startButton.SetActive(false);

        // Activate all puzzle pieces
        foreach (GameObject piece in puzzlePieces)
        {
            piece.SetActive(true);
        }

        // Start the timer
        gameStarted = true;
        isGameActive = true; // Reset game state
        timer = 0f; // Reset the timer

    }

    void UpdateTimerUI()
    {
        // Format the timer as mm:ss
        int minutes = Mathf.FloorToInt((maxTime - timer) / 60);
        int seconds = Mathf.FloorToInt((maxTime - timer) % 60);
        timerText.text = $"Time: {minutes:00}:{seconds:00}";
    }

    bool AllPiecesSnapped()
    {
        // Check if all pieces have snapped
        foreach (GameObject piece in puzzlePieces)
        {
            Snapping snappingLogic = piece.GetComponent<Snapping>(); // Correct reference to Snapping
            if (snappingLogic != null && !snappingLogic.isSnapped) // Check the 'isSnapped' status
            {
                return false; // If any piece is not snapped, return false
            }
        }

        return true; // All pieces are snapped
    }

    void TimerEnded(bool success)
    {
        gameStarted = false;
        isGameActive = false; // Set game state to inactive

        if (success)
        {
            gameMessageText.text = "Congratulations! You completed the puzzle!";
        }
        else
        {
            gameMessageText.text = "Time's up! Better luck next time.";
        }

        gameMessageText.gameObject.SetActive(true); // Make sure the message is visible
        restartButton.SetActive(true);
    }

    // Method to restart the game
    public void RestartGame()
    {
        // Reset game state
        gameStarted = false;
        timer = 0f;

        // Hide the restart button and reset other UI elements
        restartButton.SetActive(false);
        timerText.text = "Time: 07:00";

        // Deactivate puzzle pieces and reset their state
        foreach (GameObject piece in puzzlePieces)
        {
            piece.SetActive(false);
        }

        // Show the start button again
        startButton.SetActive(true);

        randomizer.ScatterSelectedParts();

        gameMessageText.gameObject.SetActive(false);
    }
}

