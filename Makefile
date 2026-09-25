# Compiler and flags
CC = g++
CFLAGS = -Wall -Wextra -Iinclude

# Directories
SRC_DIR = src
BUILD_DIR = build
BIN_DIR = bin
INCLUDE_DIR = include

# Output binary name
TARGET = $(BIN_DIR)/main

# Find all .c files in the src/ directory
SRCS = $(shell find $(SRC_DIR) -name '*.cpp')

# Map the .c filenames to .o filenames in the build/ directory
OBJS = $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.o,$(SRCS))

# Default target
all: $(TARGET)

# Link the final executable
# @mkdir -p $(@D) creates the bin/ directory if it doesn't exist
$(TARGET): $(OBJS)
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) $^ -o $@

# Compile each source file into an object file
# @mkdir -p $(@D) creates the build/ directory if it doesn't exist
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build artifacts
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)

# Phony targets prevent conflicts with files named "all" or "clean"
.PHONY: all clean
